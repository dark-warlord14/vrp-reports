# Segfault in x86_64/memset.S below SkScalerContext::getImage on Linux

| Field | Value |
|-------|-------|
| **Issue ID** | [40083821](https://issues.chromium.org/issues/40083821) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-10-15 |
| **Bounty** | $1,000.00 |

## Description

A HTML-document with the content '<rt style="-webkit-text-stroke:+21016">crash' causes a segmentation falt in Chromium 7.0.544.0 (Developer Build 61416) Built on Ubuntu running on x86_64 Ubuntu 10.10. The issue also affects current Google Chrome stable on the same machine.

Program received signal SIGSEGV, Segmentation fault.
memset () at ../sysdeps/x86_64/memset.S:1056
1056    ../sysdeps/x86_64/memset.S: No such file or directory.
        in ../sysdeps/x86_64/memset.S
(gdb) bt
#0  memset () at ../sysdeps/x86_64/memset.S:1056
#1  0x00007ffff5c9dfb6 in SkScalerContext::getImage (this=0x7ffff873ddc0, 
    origGlyph=...) at /usr/include/bits/string3.h:86
#2  0x00007ffff5c8d8cb in SkGlyphCache::findImage (this=0x7ffff8af4a00, 
    glyph=...) at third_party/skia/src/core/SkGlyphCache.cpp:314
#3  0x00007ffff5c88671 in D1G_NoBounder_RectClip (state=..., glyph=..., 
    left=<value optimized out>, top=-122)
    at third_party/skia/src/core/SkDraw.cpp:1309
#4  0x00007ffff5c89716 in SkDraw::drawPosText (this=<value optimized out>, 
    text=0x7fffffff5c82 "U", byteLength=<value optimized out>, 
    pos=0x7fffffff19d8, constY=<value optimized out>, 
    scalarsPerPosition=<value optimized out>, paint=<value optimized out>)
    at third_party/skia/src/core/SkDraw.cpp:1741
#5  0x00007ffff5c85cf4 in SkCanvas::drawPosText (this=0x7ffff8ac0400, 
    text=0x7fffffff5c80, byteLength=10, pos=0x7fffffff19d8, paint=...)
    at third_party/skia/src/core/SkCanvas.cpp:1209
#6  0x00007ffff664606a in WebCore::Font::drawGlyphs (
    this=<value optimized out>, gc=0x0, font=<value optimized out>, 
    glyphBuffer=<value optimized out>, from=<value optimized out>, 
    numGlyphs=5, point=...)
    at third_party/WebKit/WebCore/platform/graphics/chromium/FontLinux.cpp:136
#7  0x00007ffff65e709d in WebCore::Font::drawGlyphBuffer (
    this=<value optimized out>, context=0x7fffffffc200, glyphBuffer=..., 
[...]
(gdb) info registers
rax            0x7ffff8ac4018   140737365426200
rbx            0x7ffff873ddc0   140737361731008
rcx            0xffffffffffffff86       -122
rdx            0x0      0
rsi            0x0      0
rdi            0x7ffff8baffa0   140737366392736
rbp            0x7ffff8aebc18   0x7ffff8aebc18
rsp            0x7fffffff1298   0x7fffffff1298
r8             0x1fe984f8       535397624
r9             0x300000 3145728
r10            0x8      8
r11            0x7fffef1c39d6   140737204992470
r12            0x7ffff8aebc18   140737365589016
r13            0x7fffffff1340   140737488294720
r14            0x7fffffff1390   140737488294800
r15            0x7fffffff13e0   140737488294880
rip            0x7fffef1c4168   0x7fffef1c4168 <memset+2792>
eflags         0x10206  [ PF IF RF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0
gs             0x0      0
(gdb) disas $rip-40, $rip+32
Dump of assembler code from 0x7fffef1c4140 to 0x7fffef1c4188:
   0x00007fffef1c4140 <memset+2752>:    lea    -0x80(%r8),%r8
   0x00007fffef1c4144 <memset+2756>:    cmp    $0x80,%r8
   0x00007fffef1c414b <memset+2763>:    movntdq %xmm0,(%rdi)
   0x00007fffef1c414f <memset+2767>:    movntdq %xmm0,0x10(%rdi)
   0x00007fffef1c4154 <memset+2772>:    movntdq %xmm0,0x20(%rdi)
   0x00007fffef1c4159 <memset+2777>:    movntdq %xmm0,0x30(%rdi)
   0x00007fffef1c415e <memset+2782>:    movntdq %xmm0,0x40(%rdi)
   0x00007fffef1c4163 <memset+2787>:    movntdq %xmm0,0x50(%rdi)
=> 0x00007fffef1c4168 <memset+2792>:    movntdq %xmm0,0x60(%rdi)
   0x00007fffef1c416d <memset+2797>:    movntdq %xmm0,0x70(%rdi)
   0x00007fffef1c4172 <memset+2802>:    lea    0x80(%rdi),%rdi
   0x00007fffef1c4179 <memset+2809>:    jge    0x7fffef1c4140 <memset+2752>
   0x00007fffef1c417b <memset+2811>:    sfence 
   0x00007fffef1c417e <memset+2814>:    add    %r8,%rdi
   0x00007fffef1c4181 <memset+2817>:    lea    -0x535(%rip),%r11        # 0x7fffef1c3c53 <memset+1491>



## Attachments

- [mem.html](attachments/mem.html) (text/plain; charset=us-ascii, 45 B)

## Timeline

### sc...@gmail.com (2010-10-15)

Wow! Nice bug.

One-stop copy/paste: data:text/html,<rt style="-webkit-text-stroke:+21016">crash

You can tell it's nasty simply from the fact that the crash is in the middle of the unrolled memset() loop :)

Hits on Linux 32-bit M6 stable but not Windows 32-bit M6 stable for me.

### sc...@gmail.com (2010-10-15)

Possibly Linux-only. Looks like I get to take a look :)

### sc...@gmail.com (2010-10-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-16)

Why are fonts always jacked up on linux :(

### sc...@gmail.com (2010-10-18)

Dragons located in Skia... one down, one or two to go....

### sc...@gmail.com (2010-10-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-18)

Have a patch for Skia. Should get resolved soon.

### sc...@gmail.com (2010-10-18)

@aohelin: again, nice discovery. And congratulations on your provisional $1000 Chromium Security Reward :D
The reward amount here has been increased beyond the base amount because of the excellent simple repro and very good stack trace / register dump.

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

### bu...@gmail.com (2010-10-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=63010

------------------------------------------------------------------------
r63010 | cevans@chromium.org | Mon Oct 18 19:33:44 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=63010&r2=63009&pathrev=63010

Roll Skia to r607 to pick up font fixes.

BUG=59320
TEST=layout
TBR=senorblanco

Review URL: http://codereview.chromium.org/3838007
------------------------------------------------------------------------

### sc...@gmail.com (2010-10-19)

See also
http://code.google.com/p/skia/source/detail?r=606
http://code.google.com/p/skia/source/detail?r=607

Needs merging to both M7 and M8

### ao...@gmail.com (2010-10-19)

Excellent \o/

Seems to be a good month for bug- and dragon hunting :)

### in...@chromium.org (2010-10-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-21)

Mark merged to M7 and M8.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/59320?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083821)*
