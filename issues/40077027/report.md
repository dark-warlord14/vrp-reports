# cross-process memory address leak via sa_restorer

| Field | Value |
|-------|-------|
| **Issue ID** | [40077027](https://issues.chromium.org/issues/40077027) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals |
| **Platforms** | Linux |
| **Reporter** | re...@gmail.com |
| **Assignee** | jl...@chromium.org |
| **Created** | 2013-02-24 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0

Steps to reproduce the problem:
Run the attached PoC and see addresses leak (despite the execve!) from either the parent process (shell typically when run from there) or whoever last set realtime signal handlers (usually init, pid 1, at least when glibc is used).

There is a another leak not demonstrated by this PoC where fork leaks not only through sa_restorer but sa_handler as well in case the signal structure is not shared (and therefore should not leak into the child yet it does).

What is the expected behavior?
Address information should not leak across and into arbitrary processes, the PoC should report 0 ideally for all signals.

What went wrong?
When the kernel sets up a new sighand structure (either during fork or execve, i.e., it's two separate bugs) it copies the content of the old task's sighand->action into the new one without any sanitization in the fork case, and with insufficient sanitization (via flush_signal_handlers) in the execve case. The attached patch fixes both of these issues and another unrelated potential problem where one of the sighand fields wasn't initialized in the constructor but after rcu has published the new sighand instance.

Did this work before? No 

Chrome version: all  Channel: n/a
OS Version: 2.6+ with ASLR

Note that the fork bug affects systems relying on the zygote concept especially since it's an important security boundary there and while sa_restorer leaks a glibc address usually, sa_handler could leak anything else, including a PIE's address.

Note 2: userland can also proactively fix these bugs by explicitly clearing these fields. This will be important when running on older kernels that users will never update to a fixed version.

Note 3: the set up and thus eventual leak of sa_restorer is probably libc specific, we only tested with recent glibc.

Note 4: SA_RESTORER is a deprecated feature in linux, not all archs are affected, but arm and x86 are.

Note 5: these bugs were found by the latest (not yet published) development version of my size_overflow gcc plugin (more info: https://forums.grsecurity.net/viewtopic.php?f=7&t=3043), and there's probably more lurking in the shadows :).

## Attachments

- [sighand-leak.c](attachments/sighand-leak.c) (text/x-c; charset=us-ascii, 420 B)
- [sa_restorer-leak-fix.patch](attachments/sa_restorer-leak-fix.patch) (message/rfc822; charset=us-ascii, 2.1 KB)

## Timeline

### ta...@google.com (2013-02-24)

[Empty comment from Monorail migration]

### ta...@google.com (2013-02-24)

Adding the discoverers to cc.

### jl...@chromium.org (2013-02-24)

Interesting, I'll take a look tomorrow.

### jl...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-02-25)

Kees, the kernel fix for this is pretty simple, do you want to apply it in Chrome OS ?

I'm looking into mitigating this in Chrome.

### jl...@chromium.org (2013-02-25)

"There is a another leak not demonstrated by this PoC where fork leaks not only through sa_restorer but sa_handler as well in case the signal structure is not shared (and therefore should not leak into the child yet it does)."

I don't understand this part. Regardless of a shared signal structure (i.e. threads in practice), the child should inherit sa_handler from the parent. execve() is the reset boundary here. Am I missing something?

### br...@opensrcsec.com (2013-02-25)

That's correct.  The documentation for CLONE_SIGHAND notes that if it's 
absent, the child will still receive a copy of the signal handlers at 
clone() time.  The handlers are just unshared from the parent.  So there 
should be no flush_signal_handlers called in clone_sighand().

However, this behavior may be a problem for your zygote model.  If 
you don't want the signal handlers to leak to child processes, then you 
would need to clone without CLONE_SIGHAND so that you could then reset
the signal handlers in the child.

-Brad

### jl...@chromium.org (2013-02-25)

No one clones with CLONE_SIGHAND except for threads.

But in the non thread case (fork()), signal dispositions are supposed to be inherited in childs by design. This is what we want.

### jl...@chromium.org (2013-02-26)

CL up in https://codereview.chromium.org/12314117/

I'm only fixing this in the Zygote and not for the more general creation of process. This is super hairy because we need to bypass glibc's and need to know the kernel's "struct sigaction", so I don't want to impose this in general POSIX files.

### jl...@chromium.org (2013-02-26)

Kees: sorry I hadn't looked at the kernel fix properly. I don't think it's correct since it does flush signal handler in fork(). Do you mind taking care of this?

### ma...@chromium.org (2013-02-26)

Flushing in fork() sounds very wrong. It breaks POSIX in a bad way.

Flushing in exec() is a lot more reasonable. There is no particular expectation that these pointers are in any way meaningful after the entire address space has been reset by exec().

### pa...@freemail.hu (2013-02-26)

do you need a new patch from me or will you just do the obvious fix yourselves?

### jl...@chromium.org (2013-02-26)

I'll defer to Kees since he'll probably be the one patching the Chrome OS kernel, but I bet he's happy to fix it.

### ke...@chromium.org (2013-02-26)

I can take a guess, but what's the best location in exec to do the flush?

### pa...@freemail.hu (2013-02-26)

the exec path already does the flush, it's just not sufficient. that's
what the hunk in kernel/signal.c:flush_signal_handlers fixes (the fork
side 'fix' would have simply called this very same function but it is
not correct for general userland, you'd at most want that only for the
zygote based stuff like android). for reference, here's the new patch
(whitespace damaged):

--- linux-3.8-pax/fs/exec.c     2013-02-19 01:14:43.805772738 +0100
+++ linux-3.8-pax/fs/exec.c     2013-02-24 03:47:43.501052704 +0100
@@ -1043,7 +1043,6 @@
                if (!newsighand)
                        return -ENOMEM;

-               atomic_set(&newsighand->count, 1);
                memcpy(newsighand->action, oldsighand->action,
                       sizeof(newsighand->action));

--- linux-3.8-pax/kernel/fork.c 2013-02-19 01:14:44.001772749 +0100
+++ linux-3.8-pax/kernel/fork.c 2013-02-26 00:03:05.684546134 +0100
@@ -1035,7 +1035,6 @@
        rcu_assign_pointer(tsk->sighand, sig);
        if (!sig)
                return -ENOMEM;
-       atomic_set(&sig->count, 1);
        memcpy(sig->action, current->sighand->action, sizeof(sig->action));
        return 0;
 }
@@ -1726,6 +1725,7 @@
 {
        struct sighand_struct *sighand = data;

+       atomic_set(&sighand->count, 1);
        spin_lock_init(&sighand->siglock);
        init_waitqueue_head(&sighand->signalfd_wqh);
 }
--- linux-3.8-pax/kernel/signal.c       2013-02-19 01:14:44.025772750 +0100
+++ linux-3.8-pax/kernel/signal.c       2013-02-24 03:45:19.985060366 +0100
@@ -485,6 +485,9 @@
                if (force_default || ka->sa.sa_handler != SIG_IGN)
                        ka->sa.sa_handler = SIG_DFL;
                ka->sa.sa_flags = 0;
+#ifdef SA_RESTORER
+               ka->sa.sa_restorer = NULL;
+#endif
                sigemptyset(&ka->sa.sa_mask);
                ka++;
        }

### ma...@chromium.org (2013-02-26)

Flushing on fork() breaks POSIX. It is perfectly acceptable to keep using signal handlers after calling fork(). We cannot reset them at this point.

Besides, the memory layout is exactly the same in the parent and in the child process. We are not actually leaking any information that isn't already available to the child.

### re...@gmail.com (2013-02-26)

The atomic_set part of the patch causes a memory leak for me so it should probably be reverted until somebody reviews it.

### ke...@chromium.org (2013-02-26)

So we're just down to the sa_restorer part? :)

### jl...@chromium.org (2013-02-26)

I don't understand why the atomic_set would be needed. To me, flush_signal_handlers obviously misses flushing the sa_restorer and that's an obvious fix. Did I miss something?

### pa...@freemail.hu (2013-02-26)

the idea behind moving the atomic_set's was that in copy_sighand
rcu_assign_pointer is called before the atomic_set, that is, this
new sighand structure becomes visible to everyone with an
uninitialized(?) refcount (for however short period of time).

or at least that was my understanding until Emese reported today
that moving the refcount init into the slab constructor led to
leaking the sighand structures, so clearly i'm missing something
important here ;).

so to answer Kees as well, yes, we're reduced to that single hunk
fixing the sa_restorer leak and we have an open question about
this refcount initialization business but i guess you can delegate
that discussion to lkml when the time comes.

### pa...@freemail.hu (2013-02-26)

yes, we already established that ;).

yes, but this is true only until the two processes actually remain the
'same', and when i suggested the fork case i had the userland execve
model (you call it zygote i think) in mind where it is clear that even
fork is an interesting case. it's another thing that handling it in the
general kernel would be an error, but for say android i'm less sure, it's
surely less code (both in amount and fragility) than doing it in libc.

### re...@gmail.com (2013-03-06)

Hi,
Do you have an estimated schedule of how long this whole process will take?
Eventually I would like to release the new version of my plugin which found this bug which means many users would begin to trigger it as well.

### ke...@chromium.org (2013-03-07)

We'll get this fixed in the next Chrome OS update, and I'll send the patch upsteam. Should be a few days more. (We have been distracted a bit by Pwnium.)

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-03-11)

The Chrome patch has been pending for a while, I'll try to find another reviewer.

### jl...@chromium.org (2013-03-11)

Giving access to Lei.

### bu...@chromium.org (2013-03-11)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.4
Author : Kees Cook <keescook@chromium.org>
Commit : e3e071f729474b7cb7995e8009e5ab4aa4360140

Code Review +2: Julien Tinnes
Verified    +1: Kees Cook
Change-Id     : Icb92cc8a616f326f8df783b749ba1ffad24d98ce
Reviewed-at   : https://gerrit.chromium.org/gerrit/45130

CHROMIUM: signal: always clear sa_restorer on execve

When the new signal handlers are set up, the location of sa_restorer is
not cleared, leaking a parent process's address space location to
children.  This allows for a potential bypass of the parent's ASLR by
examining the sa_restorer value returned when calling sigaction().

Based on what should be considered "secret" about addresses, it only
matters across the exec not the fork (since the VMAs haven't changed until
the exec).  But since exec sets SIG_DFL and keeps sa_restorer, this is
where it should be fixed.

Given the few uses of sa_restorer, a "set" function was not written since
this would be the only use.  Instead, we use __ARCH_HAS_SA_RESTORER, as
already done in other places.

Example of the leak before applying this patch:

$ cat /proc/$$/maps
...
7fb9f3083000-7fb9f3238000 r-xp 00000000 fd:01 404469 .../libc-2.15.so
...
$ ./leak
...
7f278bc74000-7f278be29000 r-xp 00000000 fd:01 404469 .../libc-2.15.so
...
1 0 (nil) 0x7fb9f30b94a0
2 4000000 (nil) 0x7f278bcaa4a0
3 4000000 (nil) 0x7f278bcaa4a0
4 0 (nil) 0x7fb9f30b94a0
...

BUG=chromium:177956
TEST=link build, PoC fails to show leaks

[sent upstream https://lkml.org/lkml/2013/3/11/498]
[changed #ifdef for pre-3.9 defines]
Signed-off-by: Kees Cook <keescook@chromium.org>

M  kernel/signal.c

### bu...@chromium.org (2013-03-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=187659

------------------------------------------------------------------------
r187659 | jln@chromium.org | 2013-03-12T21:53:31.446091Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/process_util_posix.cc?r1=187659&r2=187658&pathrev=187659

Linux: for all signals, reset the sa_restorer field before execve().

The kernel can leak addresses in sa_restorer. Before execve, we reset
all sa_restorer to NULL.

BUG=177956
NOTRY=true

Review URL: https://chromiumcodereview.appspot.com/12314117
------------------------------------------------------------------------

### ke...@chromium.org (2013-03-12)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-03-12)

Kees, I may be OOO for a bit, so I'll let you handle it if you don't mind, but let's wait for some dev channel time before merging.

This change (r187659) is believed safe, but quite hairy.

### ke...@chromium.org (2013-03-12)

I should clarify: my Merge-Request is for the kernel side of this fix. I have verified it on a Canary build from today.


### [Deleted User] (2013-03-12)

Merge approved to 25 & 26 branches for kernel changes only.

### [Deleted User] (2013-03-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

Project: chromiumos/third_party/kernel
Branch : release-R26-3701.B
Author : Kees Cook <keescook@chromium.org>
Commit : b59191911183c66bbe8b5dc075d35351df39b2f0

Code Review  +2: Jorge Lucangeli Obes
Verified     +1: Kees Cook
Commit Queue   : Chumped
Change-Id      : Ida07c2919dc1a8e9fbcbec1454e07df86ebbe518
Reviewed-at    : https://gerrit.chromium.org/gerrit/45267

CHERRY-PICK: CHROMIUM: signal: always clear sa_restorer on execve

When the new signal handlers are set up, the location of sa_restorer is
not cleared, leaking a parent process's address space location to
children.  This allows for a potential bypass of the parent's ASLR by
examining the sa_restorer value returned when calling sigaction().

Based on what should be considered "secret" about addresses, it only
matters across the exec not the fork (since the VMAs haven't changed until
the exec).  But since exec sets SIG_DFL and keeps sa_restorer, this is
where it should be fixed.

Given the few uses of sa_restorer, a "set" function was not written since
this would be the only use.  Instead, we use __ARCH_HAS_SA_RESTORER, as
already done in other places.

Example of the leak before applying this patch:

$ cat /proc/$$/maps
...
7fb9f3083000-7fb9f3238000 r-xp 00000000 fd:01 404469 .../libc-2.15.so
...
$ ./leak
...
7f278bc74000-7f278be29000 r-xp 00000000 fd:01 404469 .../libc-2.15.so
...
1 0 (nil) 0x7fb9f30b94a0
2 4000000 (nil) 0x7f278bcaa4a0
3 4000000 (nil) 0x7f278bcaa4a0
4 0 (nil) 0x7fb9f30b94a0
...

BUG=chromium:177956
TEST=link build, PoC fails to show leaks

[sent upstream https://lkml.org/lkml/2013/3/11/498]
[changed #ifdef for pre-3.9 defines]
Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit e3e071f729474b7cb7995e8009e5ab4aa4360140)
Signed-off-by: Kees Cook <keescook@chromium.org>

M  kernel/signal.c

### bu...@chromium.org (2013-03-13)

Project: chromiumos/third_party/kernel
Branch : release-R25-3428.B
Author : Kees Cook <keescook@chromium.org>
Commit : 9e540bea041d753b6442eab3bf8a9d19465aee75

Code Review  +2: Jorge Lucangeli Obes
Verified     +1: Kees Cook
Commit Queue   : Chumped
Change-Id      : I97b6fbcbe0b50fcf8759dd2f7443b74febdf0642
Reviewed-at    : https://gerrit.chromium.org/gerrit/45265

CHERRY-PICK: CHROMIUM: signal: always clear sa_restorer on execve

When the new signal handlers are set up, the location of sa_restorer is
not cleared, leaking a parent process's address space location to
children.  This allows for a potential bypass of the parent's ASLR by
examining the sa_restorer value returned when calling sigaction().

Based on what should be considered "secret" about addresses, it only
matters across the exec not the fork (since the VMAs haven't changed until
the exec).  But since exec sets SIG_DFL and keeps sa_restorer, this is
where it should be fixed.

Given the few uses of sa_restorer, a "set" function was not written since
this would be the only use.  Instead, we use __ARCH_HAS_SA_RESTORER, as
already done in other places.

Example of the leak before applying this patch:

$ cat /proc/$$/maps
...
7fb9f3083000-7fb9f3238000 r-xp 00000000 fd:01 404469 .../libc-2.15.so
...
$ ./leak
...
7f278bc74000-7f278be29000 r-xp 00000000 fd:01 404469 .../libc-2.15.so
...
1 0 (nil) 0x7fb9f30b94a0
2 4000000 (nil) 0x7f278bcaa4a0
3 4000000 (nil) 0x7f278bcaa4a0
4 0 (nil) 0x7fb9f30b94a0
...

BUG=chromium:177956
TEST=link build, PoC fails to show leaks

[sent upstream https://lkml.org/lkml/2013/3/11/498]
[changed #ifdef for pre-3.9 defines]
Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit e3e071f729474b7cb7995e8009e5ab4aa4360140)
Signed-off-by: Kees Cook <keescook@chromium.org>

M  kernel/signal.c

### ke...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-19)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-03-19)

Requesting merge of r187659 to M26.

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### jl...@chromium.org (2013-03-26)

Dharani, ping for the M26 merge. Is the branch open ?

### dh...@chromium.org (2013-03-26)

This is a security bug and I would prefer security team to weigh in the risk and merge it to M26.

### jl...@chromium.org (2013-03-26)

Alright, approved then. This has been baking on 27 for a while, I think it's safe to merge.

### bu...@chromium.org (2013-03-26)

------------------------------------------------------------------------
r190761 | jln@chromium.org | 2013-03-26T20:58:45.672534Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/base/process_util_posix.cc?r1=190761&r2=190760&pathrev=190761

Merge 187659 "Linux: for all signals, reset the sa_restorer fiel..."

> Linux: for all signals, reset the sa_restorer field before execve().
> 
> The kernel can leak addresses in sa_restorer. Before execve, we reset
> all sa_restorer to NULL.
> 
> BUG=177956
> NOTRY=true
> 
> Review URL: https://chromiumcodereview.appspot.com/12314117

TBR=jln@chromium.org
Review URL: https://codereview.chromium.org/12851024
------------------------------------------------------------------------

### jl...@chromium.org (2013-03-26)

[Empty comment from Monorail migration]

### dh...@chromium.org (2013-03-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-01)

@re.emese: nice bug! And it's sufficiently interesting to qualify for a $1000 Chromium Security Reward, congrats!

### pa...@chromium.org (2013-04-26)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

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

This issue was migrated from crbug.com/chromium/177956?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077027)*
