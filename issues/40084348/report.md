# pdf viewer segfault after js syntax error

| Field | Value |
|-------|-------|
| **Issue ID** | [40084348](https://issues.chromium.org/issues/40084348) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-10-30 |
| **Bounty** | $1,000.00 |

## Description

Opening the attached PDF document in Google Chrome 8.0.552.23 (Official Build 64356) dev causes a renderer segmentation fault on Ubuntu 10.10 (at least 32-bit). The piece of javascript has byte 160 after "foo = 0", which likely causes something to go awry in or after handling the syntax error. Segfault comes when dereferencing a screwed up esp, and it's value can be changed by modifying the javascript expression.

Program received signal SIGSEGV, Segmentation fault.
0x01852c30 in ?? () from /opt/google/chrome/libpdf.so
(gdb) bt
#0  0x01852c30 in ?? () from /opt/google/chrome/libpdf.so
#1  0x0186a790 in ?? () from /opt/google/chrome/libpdf.so
#2  0x01847f39 in ?? () from /opt/google/chrome/libpdf.so
#3  0x01847f93 in ?? () from /opt/google/chrome/libpdf.so
#4  0x0184ada0 in ?? () from /opt/google/chrome/libpdf.so
#5  0x01848105 in ?? () from /opt/google/chrome/libpdf.so
#6  0x0184b736 in ?? () from /opt/google/chrome/libpdf.so
#7  0x0184c976 in ?? () from /opt/google/chrome/libpdf.so
#8  0x0184cc17 in ?? () from /opt/google/chrome/libpdf.so
#9  0x01835585 in ?? () from /opt/google/chrome/libpdf.so
#10 0x0182ecba in ?? () from /opt/google/chrome/libpdf.so
#11 0x0182ee27 in ?? () from /opt/google/chrome/libpdf.so
#12 0x01580425 in ?? () from /opt/google/chrome/libpdf.so
#13 0x01581a99 in ?? () from /opt/google/chrome/libpdf.so
#14 0x0157ea90 in ?? () from /opt/google/chrome/libpdf.so
#15 0x01569ac8 in ?? () from /opt/google/chrome/libpdf.so
#16 0x0155a48e in ?? () from /opt/google/chrome/libpdf.so
#17 0x0155a7c3 in ?? () from /opt/google/chrome/libpdf.so
#18 0x0154834a in ?? () from /opt/google/chrome/libpdf.so
#19 0x01547a6c in ?? () from /opt/google/chrome/libpdf.so
#20 0x08ec745d in ?? ()
#21 0x08ed1764 in ?? ()
#22 0x091becd4 in ?? ()
[...]
(gdb) info registers
eax            0xbfffda08       -1073751544
ecx            0xbfd52d20       -1076548320
edx            0xbfd52f3c       -1076547780
ebx            0x1ac5a18        28072472
esp            0xbf552f00       0xbf552f00
ebp            0xbfffd9a8       0xbfffd9a8
esi            0xbf552f10       -1084936432
edi            0x200000 2097152
eip            0x1852c30        0x1852c30
eflags         0x10282  [ SF IF RF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb) disas $eip-46, $eip+16
Dump of assembler code from 0x1852c02 to 0x1852c40:
   0x01852c02:  add    %cl,-0x3fce0fbb(%ecx)
   0x01852c08:  jmp    0x1852c2a
   0x01852c0a:  lea    0x0(%esi),%esi
   0x01852c10:  cmp    %eax,%edi
   0x01852c12:  ja     0x1852c54
   0x01852c14:  lea    0x1(%eax),%edi
   0x01852c17:  lea    0x1e(,%edi,4),%eax
   0x01852c1e:  and    $0xfffffff0,%eax
   0x01852c21:  sub    %eax,%esp
   0x01852c23:  lea    0x1f(%esp),%esi
   0x01852c27:  and    $0xfffffff0,%esi
   0x01852c2a:  mov    -0x228(%ebp),%eax
=> 0x01852c30:  mov    %edi,0x4(%esp)
   0x01852c34:  mov    %esi,(%esp)
   0x01852c37:  mov    %eax,0xc(%esp)
   0x01852c3b:  mov    -0x224(%ebp),%eax
End of assembler dump.
(gdb) print *$esi
Cannot access memory at address 0xbf552f10


## Attachments

- [js.pdf](attachments/js.pdf) (application/pdf; charset=iso-8859-1, 204 B)
- [malloc.pdf](attachments/malloc.pdf) (application/pdf; charset=binary, 65.2 KB)

## Timeline

### ao...@gmail.com (2010-10-30)

... s/'//. Likely more useful backtrace from x86_64:

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff1d1f830 in _IO_vfwprintf (s=0x7fffffff93e0, 
    format=<value optimized out>, ap=0x7fffffffc1f0) at vfprintf.c:1614
1614    vfprintf.c: No such file or directory.
        in vfprintf.c
(gdb) bt
#0  0x00007ffff1d1f830 in _IO_vfwprintf (s=0x7fffffff93e0, 
    format=<value optimized out>, ap=0x7fffffffc1f0) at vfprintf.c:1614
#1  0x00007ffff1d30138 in _IO_vswprintf (string=0x7fffffff9750 L"found '", 
    maxlen=2048, format=0x7fffbf8ac580 L"found '%s' when expecting '%s'", 
    args=0x7fffffffc1f0) at vswprintf.c:118
#2  0x00007fffece38a19 in ?? () from /opt/google/chrome/libpdf.so
#3  0x00007fffece4c94e in ?? () from /opt/google/chrome/libpdf.so
#4  0x00007fffece2fc58 in ?? () from /opt/google/chrome/libpdf.so
#5  0x00007fffece31a6e in ?? () from /opt/google/chrome/libpdf.so
#6  0x00007fffece2fdd5 in ?? () from /opt/google/chrome/libpdf.so
#7  0x00007fffece32736 in ?? () from /opt/google/chrome/libpdf.so
[...]

### sc...@gmail.com (2010-10-30)

I am all over this.

Thanks, Aki -- you're prolific :)

### sc...@gmail.com (2010-11-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-01)

Ok, I fixed a bunch of errors in the error printing routing. For the sake of documenting the factors behind the severity decision, here are the errors:
- Failure to consider EILSEQ as an error condition if the error string is not valid UTF-8.
- Failure to reset the iteration across va_list when retrying.
- Failure to enforce a sane limit on the maximum stack consumption.

I think the third issue must be why you were seeing a crash upon dereferencing %esp.

Since the condition is an OOB write, I will conservatively assign this SecSeverity-High.

Not sure if the fix will make the next M8 release, but it'll land soon.

(r619 on trunk, r620 on M8 branch)

### ao...@gmail.com (2010-11-02)

The stack consumption limit probably takes care of issues like the attached one? Many crash backtraces have in common an apparent infinite recursion followed by a segfault when making the next call, or suddenly a few different frames followed by a nasty crash like the one below.

#0  0x0000000000b38fa3 in ?? ()
#1  0x0000000003217c7c in malloc ()
#2  0x00007fffed0af5d9 in ?? () from /opt/google/chrome/libpdf.so
#3  0x00007fffed0b048a in ?? () from /opt/google/chrome/libpdf.so
#4  0x00007fffed0b07ff in ?? () from /opt/google/chrome/libpdf.so
#5  0x00007fffecf7e569 in ?? () from /opt/google/chrome/libpdf.so
#6  0x00007fffecf7e617 in ?? () from /opt/google/chrome/libpdf.so
#7  0x00007fffecf8422f in ?? () from /opt/google/chrome/libpdf.so
#8  0x00007fffecf842fb in ?? () from /opt/google/chrome/libpdf.so
#9  0x00007fffecf505d7 in ?? () from /opt/google/chrome/libpdf.so
#10 0x00007fffecf44e7e in ?? () from /opt/google/chrome/libpdf.so
#11 0x00007fffecf451b2 in ?? () from /opt/google/chrome/libpdf.so
#12 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#13 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#14 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#15 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#16 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#17 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#18 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#19 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
#20 0x00007fffecf45150 in ?? () from /opt/google/chrome/libpdf.so
[...]


### sc...@gmail.com (2010-11-03)

Argh! Crashes in the memory allocator give me heart attack!
Fortunately, in this case, it's simply that the stack is exhausted and the fatal crash off the bottom of the stack occurs in a memory allocator function.
So I don't see any security impact.
Looking very quickly at the code around the area of the infinite recursion, it appears to be a self-referential structure in PDF in the area of forms.... I can dig up more details if required.

I don't feel the need to file a separate tracking bug for a non-security issue. If it's really getting in the way of profitable testing, let me know and I can see if it's a simple fix.


### ao...@gmail.com (2010-11-03)

Thanks. I can file non-security bugs for the remaining probable null derefs and and the stack exhaustion issues later if they persist. No trouble for testing, as I've seen only a few places where the latter crash happens, and the trace is pretty easy to recognize :)

### sc...@gmail.com (2010-11-03)

Ooh, I forgot the reward decision on this one, which is....
Congratulations! I think you know the drill by now, but you've provisionally qualified for a $1000 Chromium Security Reward.

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

### ao...@gmail.com (2010-11-05)

Most excellent :)

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2011-03-21)

Google Chrome 11.0.696.16 build 78799

### js...@chromium.org (2011-10-05)

Batch update: More fuzzy classification of security bugs not affecting stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/61338?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084348)*
