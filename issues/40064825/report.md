# Security: webgl crash on mesa

| Field | Value |
|-------|-------|
| **Issue ID** | [40064825](https://issues.chromium.org/issues/40064825) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>WebGL, Internals |
| **Reporter** | mi...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2012-08-26 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

somekind of crash

**VERSION**  

Chrome Version: stable + trunk  

Operating System: 64bit precise + mesa

**REPRODUCTION CASE**

<html>
<head>
<script>
var gl = document.createElement('canvas').getContext('experimental-webgl')
var texture = gl.createTexture()
gl.bindTexture(gl.TEXTURE\_2D, texture)
gl.texImage2D(gl.TEXTURE\_2D, 6, gl.RGBA, 512, 2, 0, gl.RGBA, gl.UNSIGNED\_BYTE, null)
gl.deleteTexture(texture)
</script>
</head>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu  

Crash State:

kernel: [518206.046616] chromium-browse[21149]: segfault at 100000011 ip 00007fffebfbc750 sp 00007fffffff9568 error 4 in swrast\_dri.so[7fffebf8a000+186000]

==16627== ERROR: AddressSanitizer crashed on unknown address 0x000100000011 (pc 0x7fffd009c750 sp 0x7fffd239e4e8 bp 0x7fffe01b3080 T21)  

AddressSanitizer can not provide additional info.  

#0 0x7fffd009c750 in ?? ??:0  

Thread T21 created by T13 here:  

#0 0x55555f256d94 in \_\_interceptor\_pthread\_create ??:0  

#1 0x555557ce807b in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, unsigned long\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:0  

#2 0x555557ce7f5c in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate\*, unsigned long\*) ???:0  

#3 0x555557cf3838 in base::Thread::StartWithOptions(base::Thread::Options const&) ???:0  

#4 0x55555d3057ab in GpuProcessHost::Init() ???:0

firefox also crashes like so.

## Attachments

- [stable-x1011.txt](attachments/stable-x1011.txt) (text/plain; charset=us-ascii, 938 B)
- [x1011.html](attachments/x1011.html) (text/html; charset=us-ascii, 350 B)
- [x1011.txt](attachments/x1011.txt) (text/plain; charset=us-ascii, 3.7 KB)
- [ff1011.txt](attachments/ff1011.txt) (text/plain; charset=us-ascii, 902 B)
- [8.1-lastlevel.patch](attachments/8.1-lastlevel.patch) (text/x-diff; charset=us-ascii, 681 B)

## Timeline

### mi...@gmail.com (2012-08-26)

https://bugzilla.mozilla.org/show_bug.cgi?id=785734

### in...@chromium.org (2012-08-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-26)

Adding reward-topanel, although we'll have to see if this only affects the software rasterizer, or Mesa in general (e.g. Intel driver).

### kb...@chromium.org (2012-08-27)

Have you contacted any of the Mesa developers such as Brian Paul or Ian Romanick? Attempting to CC: Ian on this bug report here.

However this bug is handled in Chrome (blacklisting the driver?), it will be necessary to get a fix into Mesa.


### ia...@intel.com (2012-08-27)

I can't view this bug.  There was a similar report in Firefox that was 
fixed by a recent commit to Mesa (below).  This will be in the next 
stable release (8.0.5) and the next feature release (9.0) of Mesa.

commit ff996cafce511dd8a6c4e066e409c23e147a670c
Author: St

### kb...@chromium.org (2012-08-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2012-08-27)

This looks like a different issue than the one related to an overflow of the maximum number of uniform samplers.


### mi...@gmail.com (2012-08-28)

=================================================================
==25776== ERROR: AddressSanitizer crashed on unknown address 0x000100000251 (pc 0x7fffd29d9496 sp 0x7fffd49544d0 bp 0x7fffd2c83140 T22)
AddressSanitizer can not provide additional info.
    #0 0x7fffd29d9496 (/usr/lib/x86_64-linux-gnu/dri/i965_dri.so+0x2a496)
Thread T22 created by T13 here:

works on intel aswell.

### jo...@chromium.org (2012-08-28)

Re: c#6, definitely a different issue.

Stéphane, are we carrying that patch locally in CrOS?

### ja...@gmail.com (2012-08-28)

See the Mozilla bug (I can CC anyone interested with a mozilla bugzilla account), this crash is specifically about defining a mipmap level > 0 image on a texture where lower mipmap level images have not been defined. So it should be necessary to blacklist this driver. Good thing, because that would mean blacklisting the majority of Linux users (all Mesa drivers seem affected, at least Intel and LLVMpipe, and this is sec-sensitive at least on Intel)

### ja...@gmail.com (2012-08-28)

> So it should be necessary to blacklist this driver. 

sorry, I meant: So it should NOT be necessary to blacklist this driver. 

### ja...@gmail.com (2012-08-28)

FYI, here is the patch that I am applying to the Mozilla implementation of WebGL texImage2D:

+    size_t face = WebGLTexture::FaceForTarget(target);
+
+#ifdef MOZ_X11
+    if (gl->WorkAroundDriverBugs() &&
+        mIsMesa &&
+        level > 0 &&
+        !tex->HasImageInfoAt(level - 1, face))
+    {
+        return ErrorInvalidOperation("texImage2D: lower mipmap levels have not yet been defined. Rejecting this call to avoid a known bug in Mesa drivers.");
+    }
+#endif
+

Haven't investigated yet if the same is needed for copyTexImage2D or any other call.

### ma...@chromium.org (2012-08-29)

@https://crbug.com/chromium/144886#c9, we do carry that patch in Chrome OS, you did the backports, remember?

I'm looking at this issue right now, it's a different bug. I'll make a mesa-side fix.

### jo...@chromium.org (2012-08-29)

Stéphane: so is ff996cafce511dd8a6c4e066e409c23e147a670c mentioned in c#5 the upstream fix for the samplers issue we fixed locally and backported? It looked different in the patch description, that's why I thought the bug in this thread had already been fixed in upstream Mesa.

### ma...@chromium.org (2012-08-29)

Yes it's the same fix with a different message.

### jo...@chromium.org (2012-08-29)

Cool, we'll need to carry the fix for this issue in CrOS as well, I can handle that.

### ma...@chromium.org (2012-08-29)

It seems like the lastlevel computation code goes past the maximum level, and then as it gets passed onto the rest of the code, it triggers an overflow which corrupts other data structures which come next (in this case the hierarchical zbuffer).

Mesa patch is attached.

### ma...@chromium.org (2012-08-29)

As last time, let me know when I can post the mesa patch to the mesa lists and the chrome OS patch to the review site.

### ja...@gmail.com (2012-08-29)

The patch is on the Intel driver, but the testcase crashes other drivers too. At least LLVMpipe asserts on it.

### ma...@chromium.org (2012-08-30)

Yes, there is similar code duplicated in other places; I'll make other fixes once people confirm this one.

### jo...@chromium.org (2012-08-30)

Stéphane: OK to upstream in parallel to carrying the fix locally.

### ma...@chromium.org (2012-08-30)

https://gerrit.chromium.org/gerrit/#/c/31770/


### bu...@chromium.org (2012-08-30)

Commit: 7c49183ffc441c39d8a9e8f0b84866d4da9beee2
 Email: marcheu@chromium.org

Mesa: Prevent computed lastlevel from going past MAX_TEXTURE_LEVELS

When lastLevel goes past MAX_TEXTURE_LEVELS, we end up allocating space for
more than the array can contain and we corrupt our memory.

TEST=by hand
BUG=chromium:144886

Change-Id: Ic32fe38aa26e38e365176cbb377ca744fde106ed
Reviewed-on: https://gerrit.chromium.org/gerrit/31770
Tested-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Ready: Stéphane Marchesin <marcheu@chromium.org>

A	media-libs/mesa/files/8.1-lastlevel.patch
A	media-libs/mesa/mesa-8.1.0-r10.ebuild
D	media-libs/mesa/mesa-8.1.0-r9.ebuild

### in...@chromium.org (2012-09-04)

[Empty comment from Monorail migration]

### gm...@chromium.org (2012-09-04)

You shouldn't be able to call the driver with a texture MAX_TEXTURE_LEVELS (although I don't even know what that is as in ES there is only MAX_TEXTURE_SIZE).

If you can call the driver with a value > MAX_TEXTURE_SIZE then there's a bug in the command buffer.

### ke...@google.com (2012-09-05)

Assume this is 22.  

### jo...@chromium.org (2012-09-05)

Yes. Will upload the backport CL shortly.

### jo...@chromium.org (2012-09-06)

22 backport: https://gerrit.chromium.org/gerrit/#/c/32398/

### bu...@chromium.org (2012-09-07)

Commit: eb64a558772c6b4d940bf59d95b2c0cf8e2f8336
 Email: marcheu@chromium.org

BACKPORT: Mesa: Prevent computed lastlevel from going past MAX_TEXTURE_LEVELS

When lastLevel goes past MAX_TEXTURE_LEVELS, we end up allocating space for
more than the array can contain and we corrupt our memory.

TEST=by hand
BUG=chromium:144886

Change-Id: I9fd596c77eb26ac0a96dca967776b62c5f54720f
Reviewed-on: https://gerrit.chromium.org/gerrit/31770
Tested-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Ready: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-on: https://gerrit.chromium.org/gerrit/32398
Reviewed-by: Stéphane Marchesin <marcheu@chromium.org>
Tested-by: Jorge Lucangeli Obes <jorgelo@chromium.org>

A	media-libs/mesa/files/8.1-lastlevel.patch
A	media-libs/mesa/mesa-8.1.0-r10.ebuild
D	media-libs/mesa/mesa-8.1.0-r9.ebuild
M	media-libs/mesa/mesa-9999.ebuild

### jo...@chromium.org (2012-09-12)

This needs to be merged to 21 as well since we're not doing 22 on Chrome OS.

### jo...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-09-12)

Commit: a83da5b62754e5c6a3e9a9eea1a263fa5fb2cdaa
 Email: marcheu@chromium.org

BACKPORT: Mesa: Prevent computed lastlevel from going past MAX_TEXTURE_LEVELS

When lastLevel goes past MAX_TEXTURE_LEVELS, we end up allocating space for
more than the array can contain and we corrupt our memory.

TEST=by hand
BUG=chromium:144886

Change-Id: I7bd6982c599cd9ae3b91bc27dce863bf48a870c5
Reviewed-on: https://gerrit.chromium.org/gerrit/31770
Tested-by: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Antoine Labour <piman@chromium.org>
Commit-Ready: Stéphane Marchesin <marcheu@chromium.org>
Reviewed-on: https://gerrit.chromium.org/gerrit/33052
Tested-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Stéphane Marchesin <marcheu@chromium.org>

A	media-libs/mesa/files/8.1-lastlevel.patch
D	media-libs/mesa/mesa-8.1.0-r8.ebuild
A	media-libs/mesa/mesa-8.1.0-r9.ebuild
M	media-libs/mesa/mesa-9999.ebuild

### sc...@gmail.com (2012-09-25)

@miaubiz: thanks for confirming this hits the Intel driver.

Since GPU process vulnerabilities are still critical on Chrome OS (damn GPU sandbox still hasn't shipped to stable!!), we'll reward at the $3133.7 level.

This WebGL fuzzing seems to be good for some bank ;-)

### gm...@chromium.org (2012-10-03)

I'm going to make the command buffer allocate lower-level mips if they are not already allocated.

### ja...@gmail.com (2012-10-03)

Gregg, have you seen the new testcase in https://bugzilla.mozilla.org/show_bug.cgi?id=785734#c25 : "new testcase showing a crash even though all mipmap levels were defined". You're cc'd on this bug.

### gm...@chromium.org (2012-10-03)

Thanks Jacob, I missed that. Sigh.... I posted something in the private WebGL list. I'd like to get consensus on a spec change before I changing the behavior to something that is not spec compliant. 

### jo...@chromium.org (2012-10-03)

I've looked into opening bugs in the Mesa tracker, but their Bugzilla bugtracker has no way of restricting access to bugs, so I'm trying to see if I can come up with a way of explaining the bug that does not give the details of the vulnerability away.

### kb...@chromium.org (2012-10-04)

[Empty comment from Monorail migration]

### gm...@chromium.org (2012-10-04)

I am unable to repo this issue at the moment. Tried a ToT asan release build on Ubuntu 12.04 LTS with 

OpenGL renderer string: Gallium 0.4 on llvmpipe (LLVM 0x301)
OpenGL version string: 2.1 Mesa 8.1-devel

Have also tried osmesa, neither triggers any asan errors.

I have a fix, I'd just like to verify that things are bad before the fix and good after the fix.

Any ideas?

### gm...@chromium.org (2012-10-06)

So I got a machine that this fails on. After reading Daniel's comment on the WebGL forum it looks like just enforcing the spec by disallowing  width, height > MAX_TEXTURE_SIZE >> level solves the problem and is spec compliant

I'm running that change through the bots and I also uploaded a new conformance test

https://www.khronos.org/registry/webgl/sdk/tests/conformance/textures/texture-size-limit.html

### bu...@chromium.org (2012-10-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=160678

------------------------------------------------------------------------
r160678 | gman@chromium.org | 2012-10-08T19:22:53.374475Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/texture_manager_unittest.cc?r1=160678&r2=160677&pathrev=160678
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/texture_manager.cc?r1=160678&r2=160677&pathrev=160678

Make texture manager more strict.

BUG=144886


Review URL: https://chromiumcodereview.appspot.com/11074008
------------------------------------------------------------------------

### gm...@chromium.org (2012-10-08)

Should I open a new bug for this to track the merge?

### pa...@google.com (2012-10-08)

It's better to track it here, if that works for you.

### gm...@chromium.org (2012-10-08)

Sure, I just saw "Merge-Merged" already on this issue so I wasn't sure if that was going to be a problem.

I'd like to merge to M22 if there will be another M22 release and M23 for sure.

### sc...@gmail.com (2012-10-09)

Can we just merge to M23? I think that's sufficient :)
I'm also worried about Merge-Merged potentially causing us to forget, but if we do it quickly, after a successful canary, I think we're in good shape.

### bu...@chromium.org (2012-10-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=160857

------------------------------------------------------------------------
r160857 | gman@chromium.org | 2012-10-09T16:38:57.300435Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/gpu/command_buffer/service/texture_manager_unittest.cc?r1=160857&r2=160856&pathrev=160857
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/gpu/command_buffer/service/texture_manager.cc?r1=160857&r2=160856&pathrev=160857

Merge 160678 - Make texture manager more strict.

BUG=144886


Review URL: https://chromiumcodereview.appspot.com/11074008

TBR=gman@chromium.org
Review URL: https://codereview.chromium.org/11088028
------------------------------------------------------------------------

### ke...@google.com (2012-10-09)

Cleaning up labels.

### sc...@gmail.com (2012-10-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-10-03)

This issue was migrated from crbug.com/chromium/144886?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064825)*
