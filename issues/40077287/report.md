# Kernel stack info leak via the tkill and the tgkill syscalls

| Field | Value |
|-------|-------|
| **Issue ID** | [40077287](https://issues.chromium.org/issues/40077287) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2013-03-24 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0

Steps to reproduce the problem:
1. Run the attached PoC

What is the expected behavior?
No unintended kernel memory disclosure

What went wrong?
My size_overflow plugin found a new infoleak via the tkill/tgkill syscalls. It caught the bug here:

SIZE_OVERFLOW: size overflow detected in function ptr_to_compat /home/build/linux-3.2.39/arch/x86/include/asm/compat.h:206 cicus.40_5 min, count: 4
Pid: 2813, comm: gdbus Not tainted 3.2.39-cica3 #1
Call Trace:
 [<ffffffff81100b2e>] report_size_overflow+0x22/0x2e
 [<ffffffff8103331d>] ptr_to_compat+0x42/0x61
 [<ffffffff810334d2>] copy_siginfo_to_user32+0xa7/0xd5
 [<ffffffff81033ae1>] ia32_setup_rt_frame+0xbe/0x249
 [<ffffffff8100ded0>] do_signal+0x12c/0x5c

The place of the infoleak:

int copy_siginfo_to_user32(compat_siginfo_t __user *to, siginfo_t *from)
{
        ...
        put_user_ex(ptr_to_compat(from->si_ptr), &to->si_ptr);
        ...
}

I attached the proof-of-concept code which triggers the bug. It has to be run as a 32 bit application under a 64 bit kernel (I reproduced the problem under 3.8.2 as well).
The suggested fix initializes the siginfo struct in the do_tkill function (I attached the patch).

Did this work before? No 

Chrome version:   Channel: n/a
OS Version: 3.x

We would like to release the fix within a week because the public version of the plugin can trigger this bug.
I also think that there may be similar bugs in other siginfo producing functions, probably an expert should audit them.

## Attachments

- [siginfo_leak_fix-20130324.patch](attachments/siginfo_leak_fix-20130324.patch) (text/plain; charset=us-ascii, 583 B)
- [siginfo_leak_poc-20130324.c](attachments/siginfo_leak_poc-20130324.c) (text/x-c; charset=us-ascii, 920 B)

## Timeline

### sc...@gmail.com (2013-03-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-25)

scarybeasts/jln: Can one of you own applying the patch?

### jl...@chromium.org (2013-03-25)

The sandbox won't let you run a compatibility mode executable, nor would it let you call any compatibility syscalls, so we already have a workaround for this in Chrome.

Kees, do you want to take care of applying the kernel patch in Chrome OS?

### sc...@gmail.com (2013-03-25)

@jln: for my own understanding, some questions?

1) What if the executable clears long mode directly via asm and then uses syscall? Will the seccomp BPF correctly see it as a 32-bit-mode syscall and block it?

2) Outside of the sandboxed context, what do you think the risk is of leaking bits of kernel memory? Probably minimal until we have KASLR?

### jl...@chromium.org (2013-03-25)

1) Yes, we do look at ARCH and deny if it doesn't match. So you can't int 0x80 or even far call to a 32 bits segment and sysenter.

2) Leaking the stack address can still be somewhat useful for exploits. I would rather fix it.

### jl...@chromium.org (2013-03-25)

Actually, I don't know why I assumed "stack addresses" here. We leak the content, not its address. It could potentially leak anything.

### jl...@chromium.org (2013-03-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-26)

[Empty comment from Monorail migration]

### ke...@chromium.org (2013-03-26)

Yeah, I will take care of applying this to Chrome OS and sending it upstream.

### pa...@freemail.hu (2013-03-27)

i hacked up a small gcc plugin that forcibly initializes some of these variables and would like to release it 'now' (without any reference to this bug for now). is that ok with you guys?

### jl...@chromium.org (2013-03-27)

Yes, no problem.

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

bulk edit

### ke...@chromium.org (2013-04-17)

I've fixed this in Chrome OS and sent it upstream now. Thanks!

http://marc.info/?l=linux-kernel&m=136622640810847&w=2


### ke...@chromium.org (2013-04-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2013-04-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-18)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.4
Author : Emese Revfy <re.emese@gmail.com>
Commit : 59e70abe316cbb584c9aed6d405ae180c39d3531

Code Review +2: Will Drewry
Verified    +1: Kees Cook
Change-Id     : If7603776a2f5dc28dceef4034f80b6979d18ca80
Reviewed-at   : https://gerrit.chromium.org/gerrit/48390

CHROMIUM: signal: stop info leak via the tkill and the tgkill syscalls

This fixes a kernel memory contents leak via the tkill and tgkill syscalls
for compat processes.

This is visible in the siginfo_t->_sifields._rt.si_sigval.sival_ptr field
when handling signals delivered from tkill.

The place of the infoleak:

int copy_siginfo_to_user32(compat_siginfo_t __user *to, siginfo_t *from)
{
        ...
        put_user_ex(ptr_to_compat(from->si_ptr), &to->si_ptr);
        ...
}

Signed-off-by: Emese Revfy <re.emese@gmail.com>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org

BUG=chromium:223444
TEST=link build, PoC fails to show leaks

[ sent to lkml: http://marc.info/?l=linux-kernel&m=136622640810847&w=2 ]
Signed-off-by: Kees Cook <keescook@chromium.org>

M  kernel/signal.c

### sc...@gmail.com (2013-05-03)

@re.emese: thank you! And a $500 Chromium Security Reward!

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### kr...@chromium.org (2013-12-19)

[Empty comment from Monorail migration]

### kr...@chromium.org (2014-01-21)

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

This issue was migrated from crbug.com/chromium/223444?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077287)*
