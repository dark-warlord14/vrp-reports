# Linux kernel futex() memory corruption vulnerability and exploit

| Field | Value |
|-------|-------|
| **Issue ID** | [40079619](https://issues.chromium.org/issues/40079619) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, ChromeOS |
| **CVE IDs** | CVE-2014-3153 |
| **Reporter** | sc...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2014-05-26 |
| **Bounty** | $10,000.00 |

## Description

[Reporting on behalf of Pinkie Pie. After chatting to him, he's agreed to let us have first swing at this (the IBB may consider him for a reward in addition later).
Assigning to Kees speculatively.
I've run this on my Ubuntu 12.04 and it oopses at an address near one of the constants in the exploit file, so a nasty bug. I didn't expect the exploit to work because my kernel is ancient and the exploit is against the 3.14 kernel.
Note that the exploit is against a Debian kernel which does not compile in kASLR but Pinkie does demonstrate the leak of an address to defeat kASLR as a handy exploitation bonus.
Finally note that there are additional interesting / useful notes in the attached exploit file.]

---

The issue exists when after blocking in futex_wait_requeue_pi, q.rt_waiter is NULL but &rt_waiter (on the stack) has been added to various waiter lists by rt_mutex_start_proxy_lock.

This is not supposed to be possible, because setting rt_waiter to NULL indicates atomic acquisition. This is done by requeue_pi_wake_futex, which is called by futex_requeue (FUTEX_CMP_REQUEUE_PI) in two cases where the lock could be acquired immediately on behalf of some waiter rather than blocking. Meanwhile, rt_mutex_start_proxy_lock is only called from the bottom of futex_requeue, and only enqueues rt_waiter if the lock could not be acquired immediately. Since any particular FUTEX_WAIT_REQUEUE_PI is only supposed to be requeued once, those two possibilities should be mutually exclusive.

The requeue-once rule is enforced by only allowing requeueing to the futex previously passed to futex_wait_requeue_pi as uaddr2, so it's not possible to requeue from A to B, then from B to C - but it is possible to requeue from B to B.

When this happens, if (!q.rt_waiter) passes, so rt_mutex_finish_proxy_lock is never called. (Also, AFAIK, free_pi_state is never called, which is true even without this weird requeue; in the case where futex_requeue calls requeue_pi_wake_futex directly, pi_state will sit around until it gets cleaned up in exit_pi_state_list when the thread exits. This is not a vulnerability.) futex_wait_requeue_pi exits, and various pointers to rt_waiter become dangling.

I haven't actually tested this in a sandbox, but from reading the code, I believe most/all the syscalls used in the exploit are allowed by the Chromium renderer, GPU, NaCl, etc. sandbox - in particular, futex, setpriority, and prctl, without restrictions. (setpriority is overridden to allowed in those policies; the others are in the baseline policy.) Also, the exploit should be able to defeat KASLR, although it was not actually enabled in the kernel I was testing on (see comments).

I have attached an exploit for the Debian 3.14.4-1 Linux image on amd64, which manages to run some code in kernel mode and return. As discussed in the comments, it may be nontrivial to port to other kernel builds due to unpredictable compiler decisions, but I hope it demonstrates exploitability.

For the record, my exploit would be trivially defeated by SMAP, which was not present on the CPU I was testing on; I suspect it's possible to work around this at the cost of extra complexity.

## Attachments

- [fubar.c](attachments/fubar.c) (application/octet-stream, 15.0 KB)

## Timeline

### ia...@chromium.org (2014-05-26)

[Empty comment from Monorail migration]

### ia...@chromium.org (2014-05-26)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-05-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-05-27)

Please use CVE-2014-3153 for this issue.

### sc...@gmail.com (2014-05-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-05-29)

I probably should have asked sooner, but does Pinkie Pie happen to have any suggestions on what the correct fix for this would be?

### sc...@gmail.com (2014-05-29)

From Mr. Pie: "i think it's correct as long as you can't requeue twice, though i could be wrong"

### sc...@gmail.com (2014-05-29)

From Mr. Pie: "i think it's correct as long as you can't requeue twice, though i could be wrong"

### sc...@gmail.com (2014-05-29)

Will came up with a fix that seems to do the trick (below for reference), so Kees sent it immediately upstream with details.

---
If uaddr == uaddr2, then we have broken the rule of only requeueing from
a non-pi futex to a pi futex with this call. If we attempt this, then
dangling pointers may be left for rt_waiter resulting in an exploitable
condition.

This change brings futex_requeue() into line with futex_wait_requeue_pi()
which performs the same check as per 6f7b0a2a5c0fb03be7c25bd1745baa50582348ef
---

Signed-off-by: Will Drewry <wad@chromium.org>
---
 kernel/futex.c |    2 ++
 1 file changed, 2 insertions(+)

diff --git a/kernel/futex.c b/kernel/futex.c
index 08ec814..f65a49a 100644
--- a/kernel/futex.c
+++ b/kernel/futex.c
@@ -1408,6 +1408,8 @@ static int futex_requeue(u32 __user *uaddr1,
unsigned int flags,
  u32 curval2;

  if (requeue_pi) {
+ if (uaddr1 == uaddr2)
+ return -EINVAL;
  /*
  * requeue_pi requires a pi_state, try to allocate it now
  * without any locks in case it fails.

### ms...@chromium.org (2014-05-30)

I think we can change Chromium's seccomp-bpf policies to disallow FUTEX_CMP_REQUEUE_PI and the other *_PI futex operations.

glibc should only use FUTEX_CMP_REQUEUE_PI if you're using a mutex of type PTHREAD_MUTEX_PI_*_NP, and it looks like there is no code in Chromium that uses that.

### jo...@chromium.org (2014-05-30)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-06-04)

#10: the problem is third-party code, including third-party code that we don't control (such as GPU drivers) which could be using these PTHREAD mutex. As far as I understand, glibc assumes the existence of FUTEX_LOCK_PI based only on the kernel version.

I suppose we could try and crash on all *PI operations and see what happens.

Another road block is that it would be very inefficient without some modification to our BPF compiler. We currently only support checking if some bits in a bitmask are set or unset.

Given the form of futex ops (two bits (FUTEX_PRIVATE_FLAG and FUTEX_CLOCK_REALTIME) are part of a bitmask, the rest are values), we would need to extend the compiler if we don't to simply list a lot of values in the BPF program.

I'm thinking of simply crashing on FUTEX_CMP_REQUEUE_PI (its 4 versions depending on FUTEX_PRIVATE_FLAG and FUTEX_CLOCK_REALTIME) for now, and see what we can do better later.

### jl...@chromium.org (2014-06-04)

Actually, the kernel does "int cmd = op & FUTEX_CMD_MASK;" before looking at cmd. So we really need to extend the compiler.

### jl...@chromium.org (2014-06-04)

I threw together https://codereview.chromium.org/314903002 in a rush. I'm banning any bits that is not part of the normal bitmask: hopefully userland never considers |op| as being a 16 bits value and always sets the high order bits to 0.

I'm running the try bots on it to see what happens. It's likely that this CL isn't ready.

### bu...@chromium.org (2014-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9de395e4b2e4c7aed021813373544e219271b8f1

commit 9de395e4b2e4c7aed021813373544e219271b8f1
Author: jln@chromium.org <jln@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jun 04 22:25:28 2014

Linux sandbox: restrict futex operations.

First-pass at restricting futex operations. We ban FUTEX_CMP_REQUEUE_PI, as it is
not used throughout Chrome.

BUG=377392
R=mdempsky@chromium.org

Review URL: https://codereview.chromium.org/314903002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@274934 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-06-04)

------------------------------------------------------------------
r274934 | jln@chromium.org | 2014-06-04T22:25:28.652267Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/BUILD.gn?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/baseline_policy_unittest.cc?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/baseline_policy.cc?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.cc?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/sandbox_linux.gypi?r1=274934&r2=274933&pathrev=274934
   A http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/services/android_futex.h?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.h?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/syscall_parameters_restrictions.cc?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/syscall_parameters_restrictions.h?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/syscall_sets.cc?r1=274934&r2=274933&pathrev=274934
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf-helpers/syscall_sets.h?r1=274934&r2=274933&pathrev=274934

Linux sandbox: restrict futex operations.

First-pass at restricting futex operations. We ban FUTEX_CMP_REQUEUE_PI, as it is
not used throughout Chrome.

BUG=377392
R=mdempsky@chromium.org

Review URL: https://codereview.chromium.org/314903002
-----------------------------------------------------------------

### ke...@chromium.org (2014-06-05)

ToT CLs are waiting for CQ:
https://chromium-review.googlesource.com/#/q/futex+status:open

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.4
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : b4e4d7fd5725efee6cabe4c968cea1c40973180e

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I20f902aecfd3fbc6dff31f24e6e49f0657f1ddbe
Reviewed-at    : https://chromium-review.googlesource.com/202733

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.4
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 016e4b18ea8a23cc95d7d7c569faeced5d7e189f

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I9e681b7f0ad472a91e9d17ac47ca0b13d5a91de7
Reviewed-at    : https://chromium-review.googlesource.com/202732

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.14
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 0e8df8a1a2f6c9140b942ad3e2805eedce5669cc

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I55035679922aaca0c81337e83ed36dfef23934a1
Reviewed-at    : https://chromium-review.googlesource.com/202714

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-generic build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.14
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 9786eee4ad51625db617ff96ad282ab9ce08b272

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ib98f3a92d95a127e9af73db0521c054e684a8d80
Reviewed-at    : https://chromium-review.googlesource.com/202713

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-generic build

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.14
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : d4e4390c187688a791312ba462c25255479c4f87

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ifa65496df1036aac78eb169bc0476fc56435e9ac
Reviewed-at    : https://chromium-review.googlesource.com/202710

UPSTREAM: futex: Prevent attaching to kernel threads

We happily allow userspace to declare a random kernel thread to be the
owner of a user space PI futex.

Found while analysing the fallout of Dave Jones syscall fuzzer.

We also should validate the thread group for private futexes and find
some fast way to validate whether the "alleged" owner has RW access on
the file which backs the SHM, but that's a separate issue.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Dave Jones <davej@redhat.com>
Cc: Linus Torvalds <torvalds@linux-foundation.org>
Cc: Peter Zijlstra <peterz@infradead.org>
Cc: Darren Hart <darren@dvhart.com>
Cc: Davidlohr Bueso <davidlohr@hp.com>
Cc: Steven Rostedt <rostedt@goodmis.org>
Cc: Clark Williams <williams@redhat.com>
Cc: Paul McKenney <paulmck@linux.vnet.ibm.com>
Cc: Lai Jiangshan <laijs@cn.fujitsu.com>
Cc: Roland McGrath <roland@hack.frob.com>
Cc: Carlos ODonell <carlos@redhat.com>
Cc: Jakub Jelinek <jakub@redhat.com>
Cc: Michael Kerrisk <mtk.manpages@gmail.com>
Cc: Sebastian Andrzej Siewior <bigeasy@linutronix.de>
Link: http://lkml.kernel.org/r/20140512201701.194824402@linutronix.de
Signed-off-by: Thomas Gleixner &lt;tglx@linutronix.de&gt;
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-generic build

(cherry picked from commit f0d71b3dcb8332f7971b5f2363632573e6d9486a)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.14
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 21cd7898f1f433039d9c0d9caab185b83d6f0416

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I565b29d01735107162956f66e8ac0213bdc33421
Reviewed-at    : https://chromium-review.googlesource.com/202659

UPSTREAM: futex: Add another early deadlock detection check

Dave Jones trinity syscall fuzzer exposed an issue in the deadlock
detection code of rtmutex:
  http://lkml.kernel.org/r/20140429151655.GA14277@redhat.com

That underlying issue has been fixed with a patch to the rtmutex code,
but the futex code must not call into rtmutex in that case because
    - it can detect that issue early
    - it avoids a different and more complex fixup for backing out

If the user space variable got manipulated to 0x80000000 which means
no lock holder, but the waiters bit set and an active pi_state in the
kernel is found we can figure out the recursive locking issue by
looking at the pi_state owner. If that is the current task, then we
can safely return -EDEADLK.

The check should have been added in commit 59fa62451 (futex: Handle
futex_pi OWNER_DIED take over correctly) already, but I did not see
the above issue caused by user space manipulation back then.

Signed-off-by: Thomas Gleixner &lt;tglx@linutronix.de&gt;
Cc: Dave Jones &lt;davej@redhat.com&gt;
Cc: Linus Torvalds &lt;torvalds@linux-foundation.org&gt;
Cc: Peter Zijlstra &lt;peterz@infradead.org&gt;
Cc: Darren Hart &lt;darren@dvhart.com&gt;
Cc: Davidlohr Bueso &lt;davidlohr@hp.com&gt;
Cc: Steven Rostedt &lt;rostedt@goodmis.org&gt;
Cc: Clark Williams &lt;williams@redhat.com&gt;
Cc: Paul McKenney &lt;paulmck@linux.vnet.ibm.com&gt;
Cc: Lai Jiangshan &lt;laijs@cn.fujitsu.com&gt;
Cc: Roland McGrath &lt;roland@hack.frob.com&gt;
Cc: Carlos ODonell &lt;carlos@redhat.com&gt;
Cc: Jakub Jelinek &lt;jakub@redhat.com&gt;
Cc: Michael Kerrisk &lt;mtk.manpages@gmail.com&gt;
Cc: Sebastian Andrzej Siewior &lt;bigeasy@linutronix.de&gt;
Link: http://lkml.kernel.org/r/20140512201701.097349971@linutronix.de
Signed-off-by: Thomas Gleixner &lt;tglx@linutronix.de&gt;
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-generic build

(cherry picked from commit 866293ee54227584ffcb4a42f69c1f365974ba7f)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.4
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 19065919bd53ef49bd7da16bcf09f2da69df55d6

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I01210f5c56b897b722e712edd724c562a8fd8ffd
Reviewed-at    : https://chromium-review.googlesource.com/202734

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.4
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : cd846f485146e72855c103682e894f2532d514c7

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I9783980c47729de4e7921498bc7f954623644b6b
Reviewed-at    : https://chromium-review.googlesource.com/202735

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 385de850bc5497d6d35e831a502673a7828ca187

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I11d059a30d8e2a981074ddc4fd07d1c7d0e6cfa5
Reviewed-at    : https://chromium-review.googlesource.com/202697

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=link build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 1652443721d20daf0abe231f5b9bbbc652d5b5bd

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I876965ca5e206e84b65094552194e5701cd335a1
Reviewed-at    : https://chromium-review.googlesource.com/202696

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=link build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel
Branch : chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : ffb16332ff78ce90360b0d5dd8cfe83a3e6d14c5

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I840a39c4d9c6e1d234d783a61755f75d7ba99f60
Reviewed-at    : https://chromium-review.googlesource.com/202694

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=link build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel-next
Branch : chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 08f7ef8275377c3a28ab729f96853a938be47455

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I4201712421c0e5ad8b380a3eaf20c7af6693d66d
Reviewed-at    : https://chromium-review.googlesource.com/202667

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel-next
Branch : chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 03a29d580571d67a51c83db5eeac30e333cb1c01

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ide192257e6fb215a3ae936acf774d5ad13f4a1b7
Reviewed-at    : https://chromium-review.googlesource.com/202666

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel-next
Branch : chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : bfc19d26e4fa90045c0084cdc130d185f972e84a

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I9f60a0fb548081814b94a2cc6446a5563bccc303
Reviewed-at    : https://chromium-review.googlesource.com/202665

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-06)

Project: chromiumos/third_party/kernel-next
Branch : chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 04bee4e6d1d6eeb6523eb7c0981c00edf2b4af14

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ic3651b34b3066e07351e9d3bcf6b1d663af346ab
Reviewed-at    : https://chromium-review.googlesource.com/202664

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### ka...@google.com (2014-06-06)

unless this is a p0 we're not spinning m35 again so pls let me know.

### be...@chromium.org (2014-06-06)

approved for 36, though.

### dh...@chromium.org (2014-06-06)

Merge approved for M35 as well.

### ke...@chromium.org (2014-06-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-06-06)

------------------------------------------------------------------
r275491 | jln@chromium.org | 2014-06-06T18:58:33.557392Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/syscall_parameters_restrictions.cc?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/syscall_parameters_restrictions.h?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/syscall_sets.cc?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/syscall_sets.h?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/baseline_policy_unittest.cc?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/baseline_policy.cc?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.cc?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/sandbox_linux.gypi?r1=275491&r2=275490&pathrev=275491
   A http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/services/android_futex.h?r1=275491&r2=275490&pathrev=275491
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.h?r1=275491&r2=275490&pathrev=275491

Merge 274934 "Linux sandbox: restrict futex operations."

> Linux sandbox: restrict futex operations.
> 
> First-pass at restricting futex operations. We ban FUTEX_CMP_REQUEUE_PI, as it is
> not used throughout Chrome.
> 
> BUG=377392
> R=mdempsky@chromium.org
> 
> Review URL: https://codereview.chromium.org/314903002

TBR=jln@chromium.org

Review URL: https://codereview.chromium.org/317373003
-----------------------------------------------------------------

### bu...@chromium.org (2014-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b66edd015fcd9d0df571d3b6ea3fcba62535efe3

commit b66edd015fcd9d0df571d3b6ea3fcba62535efe3
Author: jln@chromium.org <jln@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jun 06 18:58:33 2014

Merge 274934 "Linux sandbox: restrict futex operations."

> Linux sandbox: restrict futex operations.
> 
> First-pass at restricting futex operations. We ban FUTEX_CMP_REQUEUE_PI, as it is
> not used throughout Chrome.
> 
> BUG=377392
> R=mdempsky@chromium.org
> 
> Review URL: https://codereview.chromium.org/314903002

TBR=jln@chromium.org

Review URL: https://codereview.chromium.org/317373003

git-svn-id: svn://svn.chromium.org/chrome/branches/1985/src@275491 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1920ff20b7bbb39ca3f42ec8cfb4b035111eb4c

commit c1920ff20b7bbb39ca3f42ec8cfb4b035111eb4c
Author: jln@chromium.org <jln@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jun 06 19:20:01 2014

Merge 275491 "Merge 274934 "Linux sandbox: restrict futex operat..."

> Merge 274934 "Linux sandbox: restrict futex operations."
> 
> > Linux sandbox: restrict futex operations.
> > 
> > First-pass at restricting futex operations. We ban FUTEX_CMP_REQUEUE_PI, as it is
> > not used throughout Chrome.
> > 
> > BUG=377392
> > R=mdempsky@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/314903002
> 
> TBR=jln@chromium.org
> 
> Review URL: https://codereview.chromium.org/317373003

TBR=jln@chromium.org

Review URL: https://codereview.chromium.org/314403003

git-svn-id: svn://svn.chromium.org/chrome/branches/1916/src@275499 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-06-06)

------------------------------------------------------------------
r275499 | jln@chromium.org | 2014-06-06T19:20:01.723892Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/syscall_sets.cc?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/syscall_sets.h?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/baseline_policy.cc?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.cc?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/sandbox_linux.gypi?r1=275499&r2=275498&pathrev=275499
   A http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/services/android_futex.h?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.h?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/syscall_parameters_restrictions.cc?r1=275499&r2=275498&pathrev=275499
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/sandbox/linux/seccomp-bpf-helpers/syscall_parameters_restrictions.h?r1=275499&r2=275498&pathrev=275499

Merge 275491 "Merge 274934 "Linux sandbox: restrict futex operat..."

> Merge 274934 "Linux sandbox: restrict futex operations."
> 
> > Linux sandbox: restrict futex operations.
> > 
> > First-pass at restricting futex operations. We ban FUTEX_CMP_REQUEUE_PI, as it is
> > not used throughout Chrome.
> > 
> > BUG=377392
> > R=mdempsky@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/314903002
> 
> TBR=jln@chromium.org
> 
> Review URL: https://codereview.chromium.org/317373003

TBR=jln@chromium.org

Review URL: https://codereview.chromium.org/314403003
-----------------------------------------------------------------

### jl...@chromium.org (2014-06-06)

I merged the Linux part to both M-36 and M-35, the revisions for the merges are r275491 and r275499 specifically.

The M-35 merge was particularly non-trivial, so I hope I got that right. I'll watch the bots.

### ke...@chromium.org (2014-06-06)

I'm adding "Merge-Approved" back for the kernel CLs, just to avoid confusion.


### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R36-5841.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : f55ed0f7c6c36c4a194723f7dd3797e420a3063b

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ie8d2823ab041a0eb7697554fd33a99d71fd846cc
Reviewed-at    : https://chromium-review.googlesource.com/202949

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit bfc19d26e4fa90045c0084cdc130d185f972e84a)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R36-5841.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 7ac9616a6bc44d4530d1dffefa1aa9fe21e6fb3c

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I16b6c04bd5cc0430ab589de67264053d0cf693cb
Reviewed-at    : https://chromium-review.googlesource.com/202948

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 04bee4e6d1d6eeb6523eb7c0981c00edf2b4af14)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel
Branch : release-R35-5712.B
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 5dc7872445247c5af825b690fc444808250a6686

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I1841c03fd575bb96c4c6c74a33b1b316870ae3a2
Reviewed-at    : https://chromium-review.googlesource.com/202945

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit b4e4d7fd5725efee6cabe4c968cea1c40973180e)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel
Branch : release-R35-5712.B
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 18b485d6e58103023776035d3482c7eab249c084

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I7dfc7008c9b8a4e3809ca3c52868234648b32aae
Reviewed-at    : https://chromium-review.googlesource.com/202944

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 016e4b18ea8a23cc95d7d7c569faeced5d7e189f)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R36-5841.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : c22a2e7c29a6175b1b17a62f54f0dd6f73531561

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I6eae135ff7ccf81f3582f6d7ab412c2b7ab5ce6d
Reviewed-at    : https://chromium-review.googlesource.com/202961

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 08f7ef8275377c3a28ab729f96853a938be47455)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 11534c0106f6a211253249a71dea6fff295be0a6

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I7c465d7e034643f615c052500b2f1528fb6a4423
Reviewed-at    : https://chromium-review.googlesource.com/202609

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 04bee4e6d1d6eeb6523eb7c0981c00edf2b4af14)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel
Branch : release-R35-5712.B
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 9531c0f073c8037ae42ebd44221de723ef95f5fb

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I198f314f5e85a02c14e009732b4d7d52b646cf5a
Reviewed-at    : https://chromium-review.googlesource.com/202946

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 19065919bd53ef49bd7da16bcf09f2da69df55d6)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 089a636c78adb45e5a2349dbff2c49c2a36736b9

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I308b07a0f0e31b3348ee6f3c72bcb5e30a930311
Reviewed-at    : https://chromium-review.googlesource.com/202940

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit bfc19d26e4fa90045c0084cdc130d185f972e84a)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 33c24e87ca663fe42a5a28da6bb3e323a561b5bd

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ic47e80285441a3c275a71e2e41b3f17f59690c68
Reviewed-at    : https://chromium-review.googlesource.com/202930

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 04bee4e6d1d6eeb6523eb7c0981c00edf2b4af14)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : f38762d0f8a15257b1c38fdb8fee2ce9ef0ae085

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I94659fc5069a1285f83878d1da06725de585ec8f
Reviewed-at    : https://chromium-review.googlesource.com/202942

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 08f7ef8275377c3a28ab729f96853a938be47455)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.10
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 57dcedefeaab0a161df10f744f0ba8677e80c94e

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ifdbd855d0d3f8128ca63f99ca50234770f0659ac
Reviewed-at    : https://chromium-review.googlesource.com/202941

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 03a29d580571d67a51c83db5eeac30e333cb1c01)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 355371d435076d99b6f5974b5149b8497e21aa66

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I56373b54d876bd82f3e32467f31aec4d436a4eb1
Reviewed-at    : https://chromium-review.googlesource.com/202932

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 03a29d580571d67a51c83db5eeac30e333cb1c01)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : b5545a230ecac25281c9a2120d625cc37fe3182b

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I42b9c2c2f7776be260ad2197bc1ac4287e021007
Reviewed-at    : https://chromium-review.googlesource.com/202931

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit bfc19d26e4fa90045c0084cdc130d185f972e84a)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel
Branch : release-R36-5841.B
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 72d72c4b092ead31d0ddcf3e8bf6e66361d07cb0

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I06f5e96c54e373e2980c8e3a024a7e8bbc079aa7
Reviewed-at    : https://chromium-review.googlesource.com/202915

UPSTREAM: futex: Validate atomic acquisition in futex_lock_pi_atomic()

We need to protect the atomic acquisition in the kernel against rogue
user space which sets the user space futex to 0, so the kernel side
acquisition succeeds while there is existing state in the kernel
associated to the real owner.

Verify whether the futex has waiters associated with kernel state. If
it has, return -EINVAL. The state is corrupted already, so no point in
cleaning it up. Subsequent calls will fail as well. Not our problem.

[ tglx: Use futex_top_waiter() and explain why we do not need to try
  	restoring the already corrupted user space state. ]

Signed-off-by: Darren Hart <dvhart@linux.intel.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit b4e4d7fd5725efee6cabe4c968cea1c40973180e)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel
Branch : release-R36-5841.B
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 0365aff53dde26c9243655b3e0be2b499cda482e

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I190973cb5ce01db3689a15c6b7c2cb2a8c869426
Reviewed-at    : https://chromium-review.googlesource.com/202914

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 016e4b18ea8a23cc95d7d7c569faeced5d7e189f)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R36-5841.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 5c07ee75a2352b11d73b0fe51e732653c13bd1fc

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : If1721711a2698551c054d5fad6b7c04581f71b4b
Reviewed-at    : https://chromium-review.googlesource.com/202604

UPSTREAM: futex: Forbid uaddr == uaddr2 in futex_requeue(..., requeue_pi=1)

If uaddr == uaddr2, then we have broken the rule of only requeueing
from a non-pi futex to a pi futex with this call. If we attempt this,
then dangling pointers may be left for rt_waiter resulting in an
exploitable condition.

This change brings futex_requeue() into line with
futex_wait_requeue_pi() which performs the same check as per commit
6f7b0a2a5 (futex: Forbid uaddr == uaddr2 in futex_wait_requeue_pi())

[ tglx: Compare the resulting keys as well, as uaddrs might be
  	different depending on the mapping ]

Fixes CVE-2014-3153.

Reported-by: Pinkie Pie
Signed-off-by: Will Drewry <wad@chromium.org>
Signed-off-by: Kees Cook <keescook@chromium.org>
Cc: stable@vger.kernel.org
Signed-off-by: Thomas Gleixner <tglx@linutronix.de>

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 04bee4e6d1d6eeb6523eb7c0981c00edf2b4af14)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel
Branch : release-R36-5841.B
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : c5eb087af2b9cafa14a9a577721c3d96ba3a73da

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ifee2b6575ddc5f5b82fc05e1ca2d45790af81d0d
Reviewed-at    : https://chromium-review.googlesource.com/202917

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=x86-alex build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit cd846f485146e72855c103682e894f2532d514c7)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R35-5712.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 945cbcd16e8bf5272f4749798ab29ac4fe6b2e39

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I1c52e069fe1c714adec3e421c535ab7ac00a93a5
Reviewed-at    : https://chromium-review.googlesource.com/202933

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from ToT commit 08f7ef8275377c3a28ab729f96853a938be47455)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R36-5841.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 8401d2aa7fa4539170da0357f6dd6b835fdb0d5c

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : I01552cd555bcbead9cea3024b382cce3c831b903
Reviewed-at    : https://chromium-review.googlesource.com/202607

UPSTREAM: futex: Make lookup_pi_state more robust

The current implementation of lookup_pi_state has ambigous handling of
the TID value 0 in the user space futex. We can get into the kernel
even if the TID value is 0, because either there is a stale waiters
bit or the owner died bit is set or we are called from the requeue_pi
path or from user space just for fun.

The current code avoids an explicit sanity check for pid = 0 in case
that kernel internal state (waiters) are found for the user space
address. This can lead to state leakage and worse under some
circumstances.

Handle the cases explicit:

     Waiter | pi_state | pi->owner | uTID      | uODIED | ?

[1]  NULL   | ---      | ---       | 0         | 0/1    | Valid
[2]  NULL   | ---      | ---       | >0        | 0/1    | Valid

[3]  Found  | NULL     | --        | Any       | 0/1    | Invalid

[4]  Found  | Found    | NULL      | 0         | 1      | Valid
[5]  Found  | Found    | NULL      | >0        | 1      | Invalid

[6]  Found  | Found    | task      | 0         | 1      | Valid

[7]  Found  | Found    | NULL      | Any       | 0      | Invalid

[8]  Found  | Found    | task      | ==taskTID | 0/1    | Valid
[9]  Found  | Found    | task      | 0         | 0      | Invalid
[10] Found  | Found    | task      | !=taskTID | 0/1    | Invalid

[1]  Indicates that the kernel can acquire the futex atomically. We
     came came here due to a stale FUTEX_WAITERS/FUTEX_OWNER_DIED bit.

[2]  Valid, if TID does not belong to a kernel thread. If no matching
     thread is found then it indicates that the owner TID has died.

[3]  Invalid. The waiter is queued on a non PI futex

[4]  Valid state after exit_robust_list(), which sets the user space
     value to FUTEX_WAITERS | FUTEX_OWNER_DIED.

[5]  The user space value got manipulated between exit_robust_list()
     and exit_pi_state_list()

[6]  Valid state after exit_pi_state_list() which sets the new owner in
     the pi_state but cannot access the user space value.

[7]  pi_state->owner can only be NULL when the OWNER_DIED bit is set.

[8]  Owner and user space value match

[9]  There is no transient state which sets the user space TID to 0
     except exit_robust_list(), but this is indicated by the
     FUTEX_OWNER_DIED bit. See [4]

[10] There is no transient state which leaves owner and user space
     TID out of sync.

Backport to 3.13
  conflicts: kernel/futex.c

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Signed-off-by: John Johansen <john.johansen@canonical.com>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from commit ToT 08f7ef8275377c3a28ab729f96853a938be47455)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### bu...@chromium.org (2014-06-07)

Project: chromiumos/third_party/kernel-next
Branch : release-R36-5841.B-chromeos-3.8
Author : Thomas Gleixner <tglx@linutronix.de>
Commit : 6d2538f62da639b480476fe9155e8c0dbf2ba929

Code-Review  0 : Kees Cook, chrome-internal-fetch
Code-Review  +2: Will Drewry
Commit-Queue 0 : Will Drewry, chrome-internal-fetch
Commit-Queue +1: Kees Cook
Verified     0 : Will Drewry, chrome-internal-fetch
Verified     +1: Kees Cook
Change-Id      : Ie11adb7056e855a23b8d2e2587c509c3a200eba0
Reviewed-at    : https://chromium-review.googlesource.com/202606

UPSTREAM: futex: Always cleanup owner tid in unlock_pi

If the owner died bit is set at futex_unlock_pi, we currently do not
cleanup the user space futex. So the owner TID of the current owner
(the unlocker) persists. That's observable inconsistant state,
especially when the ownership of the pi state got transferred.

Clean it up unconditionally.

Signed-off-by: Thomas Gleixner <tglx@linutronix.de>
Cc: Kees Cook <keescook@chromium.org>
Cc: Will Drewry <wad@chromium.org>
Cc: Darren Hart <dvhart@linux.intel.com>
Cc: stable@vger.kernel.org

BUG=chromium:377392
TEST=nyan build & boot

Signed-off-by: Kees Cook <keescook@chromium.org>

(cherry picked from commit ToT 03a29d580571d67a51c83db5eeac30e333cb1c01)
Signed-off-by: Kees Cook &lt;keescook@chromium.org&gt;

kernel/futex.c

### ke...@chromium.org (2014-06-07)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-06-10)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

Updating with reward amount of $10,000 from ChromeOS release notes.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-13)

Bulk update: removing view restriction from closed bugs.

### kr...@chromium.org (2014-09-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mw...@gmail.com (2018-09-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-09-14)

This issue was migrated from crbug.com/chromium/377392?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079619)*
