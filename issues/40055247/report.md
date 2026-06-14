# GPU process crash below DoDrawArrays (Nvidia)

| Field | Value |
|-------|-------|
| **Issue ID** | [40055247](https://issues.chromium.org/issues/40055247) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>GPU>VendorSpecific |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2012-03-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached page causes a GPU process crash. A crash like this seems to be happening in every version from stable to current unstable, but the same repros don't seem to work for all versions. The attached partially minimized testcase works at least against <https://commondatastorage.googleapis.com/chromium-browser-asan/asan-symbolized-linux-release-127410.zip>, which happened to be the latest version last time I checked.

The crash happens in normal and ASan builds.

**VERSION**  

Chrome Version: Chromium 19.0.1074.0 (Developer Build 127410)  

Operating System: Linux (Debian 6.0.4, x86\_64)  

GL\_VERSION: 4.2.0 NVIDIA 295.20

**REPRODUCTION CASE**

1. Download both files (nothing wrong with CanvasMatrix.js)
2. chrome-asan unknown-2.html
3. gpu process crashes

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x0000000040d26a68 in ?? ()  

(gdb) bt  

#0 0x0000000040d26a68 in ?? ()  

#1 0x0000000040b77000 in ?? ()  

#2 0x00007f26bf9cde00 in ?? ()  

#3 0x00000000023dc090 in ?? ()  

#4 0x0000000040b77000 in ?? ()  

#5 0x00007f26dccb444f in ?? () from /usr/lib/libnvidia-glcore.so.295.20  

#6 0x00007f26dccb5eb2 in ?? () from /usr/lib/libnvidia-glcore.so.295.20  

#7 0x00007f26f0155641 in gpu::gles2::GLES2DecoderImpl::DoDrawArrays (this=<optimized out>, instanced=<optimized out>, mode=<optimized out>,  

first=<optimized out>, count=<optimized out>, primcount=<optimized out>) at gpu/command\_buffer/service/gles2\_cmd\_decoder.cc:5229  

#8 0x00007f26f0129f88 in gpu::gles2::GLES2DecoderImpl::DoCommand (this=<optimized out>, command=<optimized out>,  

arg\_count=<error reading variable: Unhandled dwarf expression opcode 0x0>, cmd\_data=<optimized out>)  

at gpu/command\_buffer/service/gles2\_cmd\_decoder.cc:3112  

#9 0x00007f26f01ada36 in gpu::CommandParser::ProcessCommand (this=<optimized out>) at gpu/command\_buffer/service/cmd\_parser.cc:62  

#10 0x00007f26f0164c68 in gpu::GpuScheduler::PutChanged (this=<error reading variable: Unhandled dwarf expression opcode 0x0>)  

at gpu/command\_buffer/service/gpu\_scheduler.cc:69  

#11 0x00007f26ee1645ed in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (gpu::GpuScheduler::\*)()>, void (gpu::GpuScheduler\*)>::MakeItSo(base::internal::RunnableAdapter<void (gpu::GpuScheduler::\*)()>, gpu::GpuScheduler\*) (a1=<optimized out>, runnable=...)  

at ./base/bind\_internal.h:868  

#12 0x00007f26ee1644bd in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (gpu::GpuScheduler::\*)()>, void (gpu::GpuScheduler\*), void (base::internal::UnretainedWrapper[gpu::GpuScheduler](javascript:void(0);))>, void (gpu::GpuScheduler\*)>::Run(base::internal::BindStateBase\*) (  

base=<optimized out>) at ./base/bind\_internal.h:1170  

#13 0x00007f26ee15b63c in GpuCommandBufferStub::OnAsyncFlush (this=<optimized out>, put\_offset=<optimized out>, flush\_count=<optimized out>)  

at content/common/gpu/gpu\_command\_buffer\_stub.cc:429  

#14 0x00007f26ee15b3c4 in GpuCommandBufferMsg\_AsyncFlush::Dispatch<GpuCommandBufferStub, GpuCommandBufferStub, void (GpuCommandBufferStub::\*)(int, unsigned int)> (msg=<error reading variable: Unhandled dwarf expression opcode 0x1>, obj=<error reading variable: Unhandled dwarf expression opcode 0x1>,  

sender=<optimized out>, func=...) at ./content/common/gpu/gpu\_messages.h:366  

#15 0x00007f26ee158d21 in GpuCommandBufferStub::OnMessageReceived (this=<optimized out>, message=...)  

at content/common/gpu/gpu\_command\_buffer\_stub.cc:110  

#16 0x00007f26ee15c98d in non-virtual thunk to GpuCommandBufferStub::OnMessageReceived(IPC::Message const&) ()  

#17 0x00007f26ee0e7e3d in MessageRouter::RouteMessage (this=<optimized out>,  

msg=<error reading variable: DWARF-2 expression error: DW\_OP\_reg operations must be used either alone or in conjunction with DW\_OP\_piece or DW\_OP\_bit\_piece.>) at content/common/message\_router.cc:46  

#18 0x00007f26ee14ef3f in GpuChannel::HandleMessage (this=<optimized out>) at content/common/gpu/gpu\_channel.cc:250  

#19 0x00007f26ee154900 in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (GpuChannel::\*)()>, void (base::WeakPtr<GpuChannel> const&)>::MakeItSo(base::internal::RunnableAdapter<void (GpuChannel::\*)()>, base::WeakPtr<GpuChannel> const&) (a1=..., runnable=...)  

at ./base/bind\_internal.h:880  

#20 0x00007f26ed27d393 in MessageLoop::RunTask (this=<optimized out>, pending\_task=...) at base/message\_loop.cc:458  

#21 0x00007f26ed27db84 in MessageLoop::DeferOrRunPendingTask (this=<error reading variable: Unhandled dwarf expression opcode 0x0>  

pending\_task=<error reading variable: Unhandled dwarf expression opcode 0x0>) at base/message\_loop.cc:470

#22 0x00007f26ed27df3e in MessageLoop::DoWork (this=<optimized out>) at base/message\_loop.cc:660  

#23 0x00007f26ed31c6b0 in base::MessagePumpGlib::RunWithDispatcher (this=<optimized out>,  

delegate=<error reading variable: Unhandled dwarf expression opcode 0x1>,  

dispatcher=<error reading variable: DWARF-2 expression error: DW\_OP\_reg operations must be used either alone or in conjunction with DW\_OP\_piece or DW\_OP\_bit\_piece.>) at base/message\_pump\_glib.cc:210  

#24 0x00007f26ed27cbae in MessageLoop::RunInternal (this=<optimized out>) at base/message\_loop.cc:417  

#25 0x00007f26ed27b888 in MessageLoop::Run (this=<optimized out>) at base/message\_loop.cc:300  

#26 0x00007f26ed1adab7 in GpuMain (parameters=...) at content/gpu/gpu\_main.cc:132  

#27 0x00007f26ed1ac776 in (anonymous namespace)::RunNamedProcessTypeMain (  

process\_type=<error reading variable: Unhandled dwarf expression opcode 0x0>, main\_function\_params=..., delegate=<optimized out>)  

at content/app/content\_main\_runner.cc:282  

#28 0x00007f26ed1ac13c in (anonymous namespace)::ContentMainRunnerImpl::Run (this=<optimized out>) at content/app/content\_main\_runner.cc:511  

#29 0x00007f26ed1ab5bf in content::ContentMain (argc=<optimized out>, argv=<optimized out>, delegate=<optimized out>) at content/app/content\_main.cc:35  

#30 0x00007f26ebf50d37 in ChromeMain (argc=<optimized out>, argv=<error reading variable: Unhandled dwarf expression opcode 0x0>)  

at chrome/app/chrome\_main.cc:32  

#31 0x00007f26ebf50c8b in main (argc=4837440, argv=0x7f26c84b6008) at chrome/app/chrome\_exe\_main\_gtk.cc:18  

(gdb) p $rsi  

$1 = 139804545867784  

(gdb) x/10i $rip-20  

0x40d26a54: mov (%rsi),%rsi  

0x40d26a57: mov 0x388(%rsi),%rsi  

0x40d26a5e: mov %rcx,%rdi  

0x40d26a61: shl $0x4,%rdi  

0x40d26a65: add %rdi,%rsi  

=> 0x40d26a68: mov (%rsi),%edi  

0x40d26a6a: mov 0x4(%rsi),%ebp  

0x40d26a6d: mov %edi,0x10(%rax)  

0x40d26a70: mov %ebp,0x14(%rax)  

0x40d26a73: add $0x18,%rax  

(gdb) i r  

rax 0x7f26c00b9660 139804407469664  

rbx 0x40b77000 1085763584  

rcx 0x49d04 302340  

rdx 0x134b02 1264386  

rsi 0x7f26c84b6008 139804545867784  

rdi 0x49d040 4837440  

rbp 0x0 0x0  

rsp 0x7fff1abbdbd8 0x7fff1abbdbd8  

r8 0x7f26dacc0080 139804856287360  

r9 0x100000 1048576  

r10 0x0 0  

r11 0x0 0  

r12 0x17e806 1566726  

r13 0x7f26dad445f8 139804856829432  

r14 0x0 0  

r15 0x0 0  

rip 0x40d26a68 0x40d26a68  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

## Attachments

- [CanvasMatrix.js](attachments/CanvasMatrix.js) (text/plain; charset=us-ascii, 10.9 KB)
- [unknown-2.html](attachments/unknown-2.html) (text/html; charset=us-ascii, 4.2 KB)
- [repro.tar.gz](attachments/repro.tar.gz) (application/x-gzip; charset=binary, 155.5 KB)
- [unknown-3.html](attachments/unknown-3.html) (text/x-c; charset=us-ascii, 1.9 KB)

## Timeline

### [Deleted User] (2012-03-19)

Aki, can you upload the other test cases that you have. I can't get this to reproduce anywhere.

### ao...@gmail.com (2012-03-20)

Here are some more repros. repro-* cause the gpu process to crash in the corresponding version on every load in the ASan build here. Current stable and and beta (18.0.1025.113) also crash on every try with $ google-chrome rad-*.html. The crash usually looks like:

Mar 20 07:46:11 calculon kernel: [33420.144643] chrome[18924]: segfault at 7fda676b2008 ip 0000000041b5ba68 sp 00007fffb9e6c4a8 error 4 in glKFohOK (deleted)[41b5a000+2000]

or 

==19091== ERROR: AddressSanitizer crashed on unknown address 0x7f9a1e070008 (pc 0x0000411a6e28 sp 0x7fffdae46e38 bp 0x000000000000 T0)

If these don't work, do you have the same Nvidia driver?

### kc...@chromium.org (2012-03-20)

glider@, do you have nvidia 295.20? 

### gl...@chromium.org (2012-03-20)

Yes, nvidia 295.20
chrome:gpu-internals tell me the following:

Canvas: Software only, hardware acceleration unavailable
HTML Rendering: Hardware accelerated
3D CSS: Hardware accelerated
WebGL: Hardware accelerated
WebGL multisampling: Hardware accelerated

The following command line:
 $ ./chrome --user-data-dir=Chrome.tmp unknown-2.html 
does not crash for me.

### gl...@chromium.org (2012-03-20)

Some of the reproducers from repro/ indeed work with the binaries from https://commondatastorage.googleapis.com/chromium-browser-asan/asan-symbolized-linux-release-127410.zip

$ ./chrome --user-data-dir=Chrome.tmp repro/repro-125985.html 
ASAN:SIGSEGV
==28517== ERROR: AddressSanitizer crashed on unknown address 0x7fa5256be008 (pc 0x000041a9be28 sp 0x7fffff170c58 bp 0x000000000000 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x41a9be28 (/tmp/glrsO6FQ (deleted)+0x1e28)
Stats: 201M malloced (83M for red zones) by 38136 calls
Stats: 0M realloced by 2931 calls
Stats: 31M freed by 22900 calls
Stats: 0M really freed by 0 calls
Stats: 320M (81953 full pages) mmaped in 38 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:2048; 13:2560; 14:512; 15:256; 16:64; 17:96; 18:16; 19:24; 20:16; 23:4; 24:1; 25:5; 
  mallocs by size class: 8:30588; 9:1323; 10:1312; 11:696; 12:1466; 13:2061; 14:414; 15:130; 16:27; 17:72; 18:4; 19:20; 20:13; 23:4; 24:1; 25:5; 
  frees   by size class: 8:16468; 9:937; 10:1139; 11:486; 12:1349; 13:2027; 14:259; 15:120; 16:19; 17:69; 18:1; 19:17; 20:9; 
  rfrees  by size class: 
Stats: malloc large: 119 small slow: 368


$ ./chrome --user-data-dir=Chrome.tmp repro/rad-5.html 
ASAN:SIGSEGV
==28792== ERROR: AddressSanitizer crashed on unknown address 0x7f61700f1008 (pc 0x00004171fe28 sp 0x7fff6cd89998 bp 0x000000000000 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x4171fe28 (/tmp/glMbBctM (deleted)+0x4171fe28)
Stats: 180M malloced (64M for red zones) by 32018 calls
Stats: 0M realloced by 2741 calls
Stats: 10M freed by 16743 calls
Stats: 0M really freed by 0 calls
Stats: 276M (70678 full pages) mmaped in 27 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:512; 15:128; 16:64; 17:32; 18:16; 19:16; 20:8; 23:4; 24:1; 25:5; 
  mallocs by size class: 8:28509; 9:1084; 10:1121; 11:384; 12:210; 13:190; 14:325; 15:119; 16:17; 17:28; 18:4; 19:12; 20:5; 23:4; 24:1; 25:5; 
  frees   by size class: 8:14351; 9:696; 10:949; 11:174; 12:93; 13:156; 14:170; 15:109; 16:9; 17:25; 18:1; 19:9; 20:1; 
  rfrees  by size class: 
Stats: malloc large: 59 small slow: 182


$ ./chrome --user-data-dir=Chrome.tmp repro/repro-r125306.html 
ASAN:SIGSEGV
==28998== ERROR: AddressSanitizer crashed on unknown address 0x7fae774e5008 (pc 0x000040d6be28 sp 0x7fffed64b978 bp 0x000000000000 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x40d6be28 (/tmp/glOTWk1h (deleted)+0x1e28)
Stats: 194M malloced (77M for red zones) by 36167 calls
Stats: 0M realloced by 2852 calls
Stats: 24M freed by 20879 calls
Stats: 0M really freed by 0 calls
Stats: 296M (75803 full pages) mmaped in 32 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:2048; 13:2048; 14:512; 15:128; 16:64; 17:64; 18:16; 19:16; 20:8; 23:4; 24:1; 25:5; 
  mallocs by size class: 8:29525; 9:1223; 10:1238; 11:547; 12:1164; 13:1844; 14:384; 15:125; 16:22; 17:58; 18:4; 19:15; 20:8; 23:4; 24:1; 25:5; 
  frees   by size class: 8:15353; 9:836; 10:1066; 11:337; 12:1047; 13:1810; 14:229; 15:115; 16:14; 17:55; 18:1; 19:12; 20:4; 
  rfrees  by size class: 
Stats: malloc large: 95 small slow: 333


$ ./chrome --user-data-dir=Chrome.tmp repro/repro-r125306-2.html 
ASAN:SIGSEGV
==29046== ERROR: AddressSanitizer crashed on unknown address 0x7f6f5ed12008 (pc 0x0000415abe28 sp 0x7fff5b120d78 bp 0x000000000000 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x415abe28 (/tmp/glWM66md (deleted)+0x415abe28)
Stats: 180M malloced (64M for red zones) by 32036 calls
Stats: 0M realloced by 2741 calls
Stats: 10M freed by 16747 calls
Stats: 0M really freed by 0 calls
Stats: 276M (70678 full pages) mmaped in 27 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:512; 15:128; 16:64; 17:32; 18:16; 19:16; 20:8; 23:4; 24:1; 25:5; 
  mallocs by size class: 8:28528; 9:1084; 10:1120; 11:384; 12:210; 13:190; 14:325; 15:119; 16:17; 17:28; 18:4; 19:12; 20:5; 23:4; 24:1; 25:5; 
  frees   by size class: 8:14356; 9:696; 10:948; 11:174; 12:93; 13:156; 14:170; 15:109; 16:9; 17:25; 18:1; 19:9; 20:1; 
  rfrees  by size class: 
Stats: malloc large: 59 small slow: 182

+all other repro/repro-r*.html reproducers.

None of other reproducers (including repro-beta-nondet.html) do crash.

### ao...@gmail.com (2012-03-20)

@glider, rad-* are a subset of files which trigger this here in current stable and beta when opened together. Could be a timing issue if it doesn't work for others. The crash looks exactly the same as what ASan reports. I apparently forgot repro-beta-nondet.html there, which occasionally crashed also at other places in beta.

### zm...@chromium.org (2012-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-20)

Gregg, can you please have a look and see whether the draw call and its contents are legitimate or not?

### ao...@gmail.com (2012-03-20)

Attached a smaller standalone testcase with one vertex- and one fragment-shader. Some multiples of 4 as last argument on row 56 seem to end up as the low bits of the bad address. This one crashes at 0x7f...004 for me in asan builds.

### gl...@chromium.org (2012-03-21)

FTR, unknown-3.html does not crash for me.

### ao...@gmail.com (2012-03-21)

It didn't reproduce on another version here either. I was just trying to narrow down the cause with one build. For example order of variable introductions seemed to be significant, which makes this sound like a stack issue and might explain why different builds may need different repros.

### la...@google.com (2012-03-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2012-03-27)

I tried several of these test cases with a Chromium Linux continuous build (19.0.1083.0 r129223, non-ASAN). One time after running repro-beta-nondet.html (which normally pops up an alert stating "ERROR: 0:1: 'unexpected EOF': syntax error") I saw the GPU process crash, and then the browser reported that WebGL wasn't supported. Normally it pops up that alert and then the gles2_cmd_decoder starts indicating that there were attempts to access out of range vertices, so the command buffer's validation is catching any application errors.

NVIDIA's 290.10 drivers (I should upgrade to 295) with a Quadro FX 380.

Is this issue mainly reproducible with ASAN? Are any errors seen running ordinary WebGL content?


### in...@chromium.org (2012-03-28)

Reverting the mass move. It does not apply to security bugs.

### ao...@gmail.com (2012-03-30)

kbr@ out of range vertices is the usual error reported when something essential is removed or changed from a file triggering the crash. It happens with and without ASan. Probably better to look at this with ASan though, because that way the crash seems to be deterministic. There are no issues in normal WebGL content; I'm specifically looking for trouble :)

If you have trouble reproducing, I can check a version+repro pair later once I have access to the machine with a Nvidia card. https://crbug.com/chromium/118970#c10 had a good repro with some control, but I forgot to add the version against which it works...

### gl...@chromium.org (2012-03-30)

kbr@, mine Nvidia drivers are 295.20
Can you please try those?

### ao...@gmail.com (2012-04-02)

rad-5.html in repro.tar.gz of https://crbug.com/chromium/118970#c2 causes ASan to report the unknown address crash on every try using https://commondatastorage.googleapis.com/chromium-browser-asan/asan-linux-release-130109.zip and locally built 20.0.1090.0 (Developer Build 130109). A similar (0x7f...008) segfault in GPU process occurs randomly in non-asan https://commondatastorage.googleapis.com/chromium-browser-asan/asan-linux-release-130109.zip when trying to open repro/*.html.

GL_RENDERER GeForce GT 520/PCIe/SSE2
GL_VERSION  4.2.0 NVIDIA 295.20

### kb...@chromium.org (2012-04-06)

Evgeny Demidov's original annihilation example (http://www.ibiblio.org/e-notes/webgl/gpu/waves/annihilation_ext.html , linked from http://www.ibiblio.org/e-notes/webgl/gpu/contents.htm) also provokes the ASan unknown address crash. There doesn't seem to be anything in rad-5.html in particular which causes it. This is with NVIIDA's 295.33 drivers on Ubuntu 10.04 with a Quadro FX 380.

All of the similarly-derived repro-* cases crash similarly.

I'm CC'ing Piers Daniell from NVIDIA's Linux OpenGL driver team and will take this bug to track it. I don't think there's anything that can be done in Chromium about this -- all of the data being uploaded to the GPU passes validation.


### kb...@chromium.org (2012-04-06)

[Empty comment from Monorail migration]

### pi...@gmail.com (2012-04-06)

When gl.drawArrays(gl.TRIANGLES, 0, 6*n1*n1); is called there are three vertex attribute arrays enabled; 0, 1 and 2. The vertex attribute pointer for vertex attrib arrays 0 and 1 source a VBO that is only 64 bytes in size. The program in use when this drawArrays is called only needs vertex attrib array 2 enabled.

It appears Chrome is attempting to compensate for this app bug by binding a "reserved" VBO before drawArrays() is called. I see a call to glBindBuffer(GL_ARRAY_BUFFER, 1); glBufferData(GL_ARRAY_BUFFER, 25067616, 0x00000000, GL_DYNAMIC_DRAW); glVertexAttribPointer(0, 4, GL_FLOAT, 0, 0, 0x00000000); to make vertex attrib array 0 safe. However, it missed calling glVertexAttribPointer(1, 4, GL_FLOAT, 0, 0, 0x00000000); to make vertex attrib array 1 safe. I think this is a Chrome bug. My guess is that it didn't account for two vertex attrib arrays bound to the same VBO.

The annihilation_ext app could also be modified to only enable the vertex attribute arrays it needs for the program in use. At the time gl.drawArrays(gl.TRIANGLES, 0, 6*n1*n1); is called, only vertex attribute array 2 needs to be enabled.

I think if the Chrome GPU data validation code is fixed this page should work fine.

There is also a driver bug which didn't safe-guard this out-of-bounds access in the robustness context. We need to fix our side too.


### gm...@chromium.org (2012-04-06)

Chrome doesn't supply data for 0 and 1. Instead it simulates Atrrib0 being off.

If Attrib0 is enabled then we validate there's enough data for the draw call
If Attrib0 is disabled then we have to fill it with the correct constant because unlike OpenGL ES, desktop OpenGL requires Attrib 0 is always enabled.

Attrib1 we don't do anything for as it's not special. Either it's enabled, in which case we validate there's enough data for the draw call. Or else it's disabled, in which case there's nothing to check.


### gm...@chromium.org (2012-04-06)

I should make it clear, there are 3 settings

1) An attrib is enabled or disabled
2) An attrib has enough data for the draw call
3) An attrib is "consumed"  (or used) by the program.

So for example 
If an attrib is disabled, no data is read, no check needed.
If an attrib is enabled but NOT consumed, no data is read, no check needed.
If an attrib is consumed and enabled we validate there's enough data for the draw

The only exception is  Attrib0 which has to be on for DesktopGL. For that one

1) If attrib0 is enabled, and consumed, check there's enough data for the darw
2) If attrib0 is enabled but not consumed, no check needed,
3) If attrib0 is disabled, make a buffer large enough for the draw and fill it with the correct constant 

It's possible #2 is the issue?  We've assumed it doesn't matter but maybe since attrib0 is special it always reads that data even when not consumed?


### gm...@chromium.org (2012-04-06)

So, maybe we finally get it. When we SimulateAttrib0 we don't fill out the buffer if it's not used (ie, if the shader-program does not consume attrib0.)  But the driver IS lazily allocating that buffer. Since we never upload data it never allocates the buffer and crashes.

It's a one line change to always fill out the buffer. We'll see if it fixes this.

### pi...@gmail.com (2012-04-07)

> If an attrib is enabled but NOT consumed, no data is read, no check needed.
A check is needed here because we do consume all enabled vertex attrib array regardless of whether the program in use reads the data. So if you add the missing glVertexAttribPointer(1, ...) call to use your substitute data you'll be in good shape. 

Using non-NULL for your substitute glBufferData call may hide the problem, but missing vertex will still be consumed. It may hide the problem because our driver may use the GPU to pull the vertex data which has bounds checking built in. Still, it's best to just point all enabled vertex attrib arrays a complete data. 

### bu...@chromium.org (2012-04-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=131538

------------------------------------------------------------------------
r131538 | gman@chromium.org | Mon Apr 09 22:48:28 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=131538&r2=131537&pathrev=131538

Always write data to new buffer in SimulateAttrib0

This is to work around linux nvidia driver bug.

TEST=asan
BUG=118970


Review URL: http://codereview.chromium.org/10019003
------------------------------------------------------------------------

### sc...@gmail.com (2012-04-10)

Nice. Maybe we can merge this to M19, seems simple? I can do it if we want.

### kb...@chromium.org (2012-04-10)

I think an M19 merge would be warranted; Chris, would definitely appreciate your help with this.

Since gman diagnosed and fixed this, assigning to him for disposition. I think we could safely mark this as Fixed, as NVIDIA knows what needs to change on their end.


### kb...@chromium.org (2012-04-12)

[Empty comment from Monorail migration]

### ja...@gmail.com (2012-04-12)

Thanks for letting us know.

Doesn't this have more far-reaching implications for WebGL, as content could exploit it by doing a WebGL bufferData call? Assuming I'm getting this right, we need to work around this at the level of the OpenGL interface, in glBufferData, not just in this specific WebGL code.

### kb...@chromium.org (2012-04-12)

It doesn't at least in Chrome and I doubt it does in Firefox. WebGL's requirement that buffers be zeroed upon allocation means that if JS calls bufferData(target, size, usage), it will actually upload a bunch of zeros to the GPU, meaning that the buffer will actually be the desired size. The bug only affected Chrome's emulation of vertex attribute 0 containing constant values.


### ja...@gmail.com (2012-04-12)

Ah yes, good point. But I'm still concerned that we might have other uses in the future for glBufferData(...,null,...) so I'll probably still do the workaround at that level.

### sc...@gmail.com (2012-04-19)

Status -> FixUnreleased since we're in good shape once we've merged the workaround. We'll take care of the merge.

### sc...@gmail.com (2012-04-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-04-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=134511

------------------------------------------------------------------------
r134511 | cevans@chromium.org | Sun Apr 29 23:55:27 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=134511&r2=134510&pathrev=134511

Merge 131538 - Always write data to new buffer in SimulateAttrib0

This is to work around linux nvidia driver bug.

TEST=asan
BUG=118970


Review URL: http://codereview.chromium.org/10019003

TBR=gman@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10268004
------------------------------------------------------------------------

### sc...@gmail.com (2012-05-04)

Thanks Aki. Since we were able to devise and ship a simple workaround, this definitely requires reward :)
$500

### sc...@gmail.com (2012-05-06)

Reward to be upped to $1337 and donated to Red Cross.

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### sc...@gmail.com (2012-05-26)

$1337 paid to American Red Cross

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/118970?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>GPU>VendorSpecific]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055247)*
