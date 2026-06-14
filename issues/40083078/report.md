# segmentation fault in bundled pdf plugin

| Field | Value |
|-------|-------|
| **Issue ID** | [40083078](https://issues.chromium.org/issues/40083078) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-09-07 |
| **Bounty** | $1,000.00 |

## Description

Viewing the attached PDF document causes a segmentation fault somewhere in libpdf.so. The error occurs at least in Ubuntu 10.04 (x86_64) with Google Chrome 7.0.503.1 (Official Build 57041) dev.

No backtrace, because I do not have debugging symbols for Chrome yet.

## Attachments

- [segv.pdf](attachments/segv.pdf) (application/pdf; charset=binary, 164.7 KB)
- [yannis_sample11.pdf](attachments/yannis_sample11.pdf) (application/pdf; charset=binary, 87.1 KB)
- [segv-2.pdf](attachments/segv-2.pdf) (application/pdf; charset=binary, 53.1 KB)

## Timeline

### sc...@gmail.com (2010-09-07)

I'll have a look at this as I'm working on PDF security. It may hopefully be something we've already caught :)

Did you generate this file through fuzzing?

BTW, note that you might not ever get debugging symbols for this because libpdf.so is a binary-only component. Pasting faulting instruction, faulting addresss and register content at the time of the crash might be interesting, still.

### ao...@gmail.com (2010-09-07)

Yes, this was fuzzed. I started a test yesterday after noticing the pdf viewer is now in google-chrome-unstable package. Nice to get a sandboxed pdf viewer. This file was the first reproducible segfault. 

Program received signal SIGFPE, Arithmetic exception.
0x01727edc in ?? () from /opt/google/chrome/libpdf.so
(gdb) info registers
eax            0x4      4
ecx            0x0      0
edx            0x0      0
ebx            0xab13c9c        179387548
esp            0xbfffd364       0xbfffd364
ebp            0xbfffd374       0xbfffd374
esi            0x41     65
edi            0xab13c9c        179387548
eip            0x1727edc        0x1727edc
eflags         0x10246  [ PF ZF IF RF ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb) disas $eip-8, $eip+16
Dump of assembler code from 0x1727ed4 to 0x1727eec:
   0x01727ed4:  add    $0xe8,%al
   0x01727ed6:  push   %ss
   0x01727ed7:  (bad)  
   0x01727ed8:  (bad)  
   0x01727ed9:  pushl  (%ecx)
   0x01727edb:  (bad)  
=> 0x01727edc:  divl   0x4(%ebx)
   0x01727edf:  mov    0x10(%ebp),%eax
   0x01727ee2:  mov    %edx,%ecx
   0x01727ee4:  mov    %edx,(%eax)
   0x01727ee6:  mov    (%ebx),%edx
   0x01727ee8:  xor    %eax,%eax
   0x01727eea:  test   %edx,%edx
End of assembler dump.

In case they are of use, segfault at ffffffffffffffe8 ip 0000000000dede1d (?), and general protection error at ip:7f27b063a51c were the non-easily-reproducible ones so far.

### ao...@gmail.com (2010-09-07)

Curious. I thought I mixed up files with the repro of #54632, but this really does give SIGFPE on my x86, whereas the x86_64 test laptop shows:
Sep  7 23:36:27 lenopad kernel: [109355.736782] chrome[20707]: segfault at 27508 ip 00007f5fda3614cb sp 00007fff1524b790 error 4 in libpdf.so[7f5fda16d000+453000]
[...]
Sep  7 23:36:27 lenopad kernel: [109355.736860] Pid: 20707, comm: chrome Not tainted 2.6.32-24-generic #42-Ubuntu 74663SG
Sep  7 23:36:27 lenopad kernel: [109355.736863] RIP: 0033:[<00007f5fda3614cb>]  [<00007f5fda3614cb>] 0x7f5fda3614cb
Sep  7 23:36:27 lenopad kernel: [109355.736870] RSP: 002b:00007fff1524b790  EFLAGS: 00010206
Sep  7 23:36:27 lenopad kernel: [109355.736873] RAX: 0000000000000004 RBX: 00000000052a6cf8 RCX: 0000000000000004
Sep  7 23:36:27 lenopad kernel: [109355.736875] RDX: 00000000000274e8 RSI: 0000000000000041 RDI: 00000000052a6cf8
Sep  7 23:36:27 lenopad kernel: [109355.736878] RBP: 0000000000000041 R08: 00000000fffeac28 R09: 00000000000000fa
Sep  7 23:36:27 lenopad kernel: [109355.736880] R10: 0000000000000033 R11: 00007f5fda4daca5 R12: 00007fff1524b7bc
Sep  7 23:36:27 lenopad kernel: [109355.736883] R13: 0000000000000000 R14: 0000000000000041 R15: 00000000052a6cf8
Sep  7 23:36:27 lenopad kernel: [109355.736886] FS:  00007f5fe5a807e0(0000) GS:ffff880028280000(0000) knlGS:0000000000000000
Sep  7 23:36:27 lenopad kernel: [109355.736889] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
Sep  7 23:36:27 lenopad kernel: [109355.736891] CR2: 0000000000027508 CR3: 0000000135d87000 CR4: 00000000000406e0
Sep  7 23:36:27 lenopad kernel: [109355.736894] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
Sep  7 23:36:27 lenopad kernel: [109355.736896] DR3: 0000000000000000 DR6: 00000000ffff0ff0 DR7: 0000000000000400


### sc...@gmail.com (2010-09-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-07)

I see pretty clear memory corruption, which would explain the varying symptoms observed.

For me on 64-bit with a plain old glibc malloc() build, I get:

export MALLOC_CHECK_=0


Program received signal SIGSEGV, Segmentation fault.
0x00007ffff713c45d in _int_malloc () from /lib/libc.so.6
(gdb) bt
#0  0x00007ffff713c45d in _int_malloc () from /lib/libc.so.6
#1  0x00007ffff713e3c0 in malloc () from /lib/libc.so.6


(gdb) disass $rip,$rip+10
Dump of assembler code from 0x7ffff713c45d to 0x7ffff713c467:
=> 0x00007ffff713c45d <_int_malloc+93>: mov    0x8(%rbx),%eax
   0x00007ffff713c460 <_int_malloc+96>: lea    0x10(%rbx),%r12
   0x00007ffff713c464 <_int_malloc+100>:        and    $0xfffffffffffffff8,%eax
End of assembler dump.
(gdb) i r
rax            0x4      4
rbx            0x14ff00001e460  369367187580000

Nice... I'll check if this is a duplicate of our internal fuzzing efforts or not.

### sc...@gmail.com (2010-09-08)

@aohelin: ah nice job! This does not appear to be a duplicate of anything we were aware of. We'll get the rewards panel to consider it.

Would you be so kind as to attach the original uncorrupted PDF which you are mutating from?

### ao...@gmail.com (2010-09-09)

The source file seems to have been http://www.tug.org/texshowcase/yannis_sample11.pdf.

Automatic minimization didn't do much to the triggering file when I tried yesterday. The file came from stutr module of the radamsa fuzzer, so luckily it is based on just one of the sample files and has fairly simple mutations. Stutr repeats an increasing or constant length suffix of the file one or more times at one or more positions.

### sc...@gmail.com (2010-09-09)

@aohelin: are you sure? yannis_sample11.pdf is 87.1 KB but segv.pdf is 164 KB

### sc...@gmail.com (2010-09-09)

@aohelin, oh ignore me. I see the mutation involved would grow the size of the file :)

### ao...@gmail.com (2010-09-09)

Does the crash, if any, caused by this file look like the same bug? I have a bunch of files to check whether they are duplicates of this issue, and most of them appear to be derived from the above sample file with the same fuzzer module. This is one of the files which is not.

### sc...@gmail.com (2010-09-10)

segv-2.pdf does seem different, but it looks like a plain old NULL to me and also looks to be fixed on PDF trunk (I can't reproduce it with a recent internal PDF build).

### ao...@gmail.com (2010-09-10)

Ok, thanks. The rest of the cases are most likely duplicates of this issue and the above null deref.

### sc...@gmail.com (2010-09-15)

Aki -- congratulations! This bug has qualified for a $1000 Chromium Security Reward.

I'm just going to mark the status as "Fixed". I've verified that our internal build now handles the PDF without any adverse affects. I'm not sure when that fix will roll into a Chrome build, but it will certainly be before we turn the PDF plugin on by default :)


### ao...@gmail.com (2010-09-16)

Most excellent. Nice doing business with you again :)

### sc...@gmail.com (2010-09-22)

Payment is in the electronic system.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/54691?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/54632]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083078)*
