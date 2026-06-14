# Linux setuid sandbox allows local privilege escalation

| Field | Value |
|-------|-------|
| **Issue ID** | [40089009](https://issues.chromium.org/issues/40089009) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | da...@gmail.com |
| **Assignee** | jl...@chromium.org |
| **Created** | 2011-03-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

On Linux systems that have some form of automated cleanup of /tmp (via cronjob or daemon), it appears to be possible to exploit the setuid chrome-sandbox application to escalate privileges to root.

**VERSION**  

Chrome Version: 9.0.597.107 (Official Build 75357)  

Operating System: Linux

**REPRODUCTION CASE**  

By exploiting two race conditions in the chrome-sandbox, it seems possible to cause arbitrary applications, to be sandboxed in a directory whose contents are entirely controlled by the local user, which can be easily be exploited to escalate privileges (e.g. by launching a setuid app that doesn't expect to be in a chroot'd environment).

First, the sandbox creates a temporary directory:

const char\* temp\_dir = mkdtemp(tempDirectoryTemplate);

At this point, the attacker must win the first race and send a SIGSTOP to the process, causing it to sleep. The attacker then waits as long as necessary for the /tmp directory to be cleaned up by something like tmpwatch. At this point, the attacker replaces the previous directory with a symlink to a directory he controls, which has been set up ahead of time to contain hard links to whatever resources he wishes to exploit once the chroot is set up.

Next, the attacker's symlinked directory is opened:

const int chroot\_dir\_fd = open(temp\_dir, O\_DIRECTORY | O\_RDONLY);

Now, the attacker must win the second race, which involves replacing this symlink with a new, empty directory, so the following call to rmdir succeeds:

if (rmdir(temp\_dir)) {

From this point forward, the attacker is home free. The attacker's directory is chown'd to root:root and chmod'd 0000, which doesn't matter because we've already pre-populated the directory with whatever we want in it. Note that this can alternatively be used to wreak havoc on a system by chown'ing and chmod'ing arbitrary directories. Assuming the child process does the proper socket communication to negotiate setting up the chroot, it seems like this would result in the child process being chroot'd to the attacker's directory, at which point a setuid process can be exec'd and exploited.

In my testing, it seems the chmod 0000 does nothing to prevent a process that is chroot'd via /proc/self/fd/X to access the new filesystem hierarchy. It's definitely possible I've missed something that would render this non-exploitable, but it seems that at the very least, it's possible to destroy a system by rendering important directories unreadable.

## Timeline

### js...@chromium.org (2011-03-17)

CCing the relevant people.

### wa...@chromium.org (2011-03-17)

After talking with Dan, I'm not sure about the exploitability beyond doing damage to the system (chmod 000 /etc/pam.d or /), but I wouldn't rule it out without more digging.

That aside, an O_NOFOLLOW would mostly resolve the mkdtemp/open issue, but I'm not sure it'd be a 100% fix.

### da...@gmail.com (2011-03-17)

On taking a closer look, it seems the chmod 0000 might hinder privilege escalation.  It might be possible to play games with fexecve() though.

### jl...@chromium.org (2011-03-17)

I mentioned this a while ago when the setuid sandbox was reimplemented for Chrome. In the original design (http://code.google.com/p/setuid-sandbox/), the empty directory is fixed.

I think we should do the same and have something like /opt/google/chrome/empty_dir instead of playing with /tmp.

(Also for security in depth, now that (I believe), we don't need LD_PRELOAD forwarding anymore, we could also execve() the renderer directly instead of using argv[1]).

### jl...@chromium.org (2011-03-17)

Forgot to add Adam and Markus.

Markus I think you specifically said that the /tmp cleaning should not be an issue on our target distributions IIRC?

### ag...@chromium.org (2011-03-17)

We should call setuid(0) in the sandbox. This stops non-root from sending signals to us (and is a standard SUIDism that I missed.)

In this case, the user can't SIGSTOP the sandbox. A tmp cleaner won't touch the temp dir unless it's sufficiently old (several hours). Thus the attacker would have to cause the sandbox to freeze for hours without SIGSTOP. That might be possible so other solutions might be called for. However a fixed directory was rejected because of the pain that it causes packagers of Chromium. It would be sad to impose that on them.

### ma...@chromium.org (2011-03-17)

Is that even necessary? I just tried writing a simple setuid-root program, and I cannot send any signals to it.

### da...@gmail.com (2011-03-17)

Yes, it's necessary, because AFAIK on Linux signal reception is based on uid, not euid.  In addition, you should also specifically ignore signals, or the controlling terminal can still sleep the process with ctrl+z.

### ag...@chromium.org (2011-03-17)

Normally a SUID binary has its effective UID set to the owner of the inode, but the real UID is preserved. kill(2) requires that "the real or effective user ID of the sending process must equal the real or saved set-user-ID of the target process".


p$ cat t.c
#include <unistd.h>
#include <stdio.h>

int
main() {
  printf("hi there\n");
  printf("uid: %d, euid: %d\n", getuid(), geteuid());
  printf("my pid is: %d\n", getpid());
  sleep(20);
  printf("goodbye\n");
  return 0;
}

$ gcc t.c -Wall
(in root shell: # chown root ./a.out && chmod u+s ./a.out)

$ ./a.out 
hi there
uid: XXXX, euid: 0
my pid is: 8494

$ kill -SEGV 8494
(works)


### ma...@chromium.org (2011-03-17)

Actually, something funny is going on with SIGSTOP. I think, it sometimes still makes it through. It probably has something to do with how PTYs work, but I haven't been able to 100% pinpoint what is going on.

So, we might want to be more paranoid. Isn't there a way to securely create a new directory? Let me think about that.

### da...@gmail.com (2011-03-17)

As Will said, adding an O_NOFOLLOW on the directory opening should resolve the issue.  This is only exploitable for anything if the sandbox opens a directory via symlink and that symlink is then replaced with a real directory for the rmdir().  If the attacker puts an actual directory there instead of a symlink, the call to rmdir() will fail and nothing bad will happen.

### jl...@chromium.org (2011-03-17)

Yes, the signal check in the kernel is very relaxed (unlike the ptrace() one), you can send signals as long as you have the same uid.

Adam: it's actually often not a good thing to setuid(0) in a setuid binary because it makes it non compatible with file capabilities. (Also countless people have been bitten by RLIMIT_NO_FILE when they did setuid(uid) to drop privileges after that without checking the return value).

You cannot rely on a setuid binary to not be stoppable. For instance the attacker controls STDOUT and could make you block on any output (including one due to an environment variable prompting glibc to issue debug messages).

### ma...@chromium.org (2011-03-17)

I can't really think of anything better either. Maybe, sanity checking the output of "stat("..", &sb)" would help. But I am not yet 100% convinced that makes a real difference.

### da...@gmail.com (2011-03-17)

It doesn't seem like it would, assuming you're trying to check that the parent directory is /tmp, because the attacker could just create his directory in /tmp.

### jl...@chromium.org (2011-03-17)

Markus: and same uid is not even necessary.

From our original discussion on this, I said:

"Markus argument about those scripts not cleaning recently created
directory is sound but an attacker could also SIGSTOP the setuid
sandbox and SIGCONT one week later."

And then I explained that being in the same session is enough for SIGSTOP anyway.


### ma...@chromium.org (2011-03-17)

Can somebody try to poke holes into the following:

#define _GNU_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <sched.h>

#include "linux_syscall_support.h"

static int fn(void *arg) {
  int *fds = (int *)arg;
  close(fds[1]);
  read(fds[0], fds, 1);
  char buf[80];
  sprintf(buf, "/proc/%d/fdinfo", getpid());
  if (chdir(buf) < 0) {
    sprintf(buf, "/proc/%d", getpid());
    chdir(buf);
  }
  chroot(".");
  _exit(0);
}

int main(int argc, char *argv[]) {
  int fds[2];
  pipe2(fds, O_CLOEXEC);
  char stack[4096];
  sys_clone(fn, stack + sizeof(stack), CLONE_FS, fds, 0, 0, 0);
  close(fds[0]);
  char *n_argv[] = { "-sash", NULL };
  execve("/bin/sash", n_argv, environ);
  puts("FAILED");
  _exit(1);
}


### jl...@chromium.org (2011-03-17)

You made the same mistake again.

chroot(".") does not work in this environment, because you share FS with an untrusted process.

### jl...@chromium.org (2011-03-17)

Otherwise, I like your idea (I'll take a better look though), provided that:

- *first* we try to chroot to /opt/google/chrome/guanrateed_empty (we open, check it's empty, root owned etc, then chroot to the fd)
- if that's not available (repackaging), we chroot to a subdir in /proc as you suggest
- we chroot to /proc/self/fdinfo instead. If something crazy happens with procfs, at least the "name" /proc/self/fdinfo won't land us in another process.

### ma...@chromium.org (2011-03-17)

Sorry for the brevity of the sample code, but thanks for pointing this out.

In a fully-implemented sandbox, we would want to delay calling exec() until after chroot(".") has successfully completed. I think, our chrome-sandbox already has an IPC mechanism that does this correctly.

### jl...@chromium.org (2011-03-17)

I think you are confused. You can't call exec() until after chroot(".")

The way I designed it (the original implementation is at http://code.google.com/p/setuid-sandbox/source/browse/trunk/s), was that you get send a "CHROOTME" message on a socketpair indeed. But this needs to happen after exec of course.

Which is also why this design is so scary and the chroot code should be minimal. In http://code.google.com/p/setuid-sandbox/source/browse/trunk/privdrop.c it's only a couple of lines running while we share FS with an untrusted process. And RLIMIT_NOFILE also helps.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### jl...@chromium.org (2011-03-22)

[Empty comment from Monorail migration]

### jl...@chromium.org (2011-03-24)

http://codereview.chromium.org/6731031/ is up for review.

### sc...@gmail.com (2011-03-28)

Chatted to jln@ -- it's a probable local privesc but very tricky to exploit so we can probably let this roll into M12.

Landed for jln@: http://codereview.chromium.org/6683056 / http://src.chromium.org/viewvc/chrome?view=rev&revision=79618

### sc...@gmail.com (2011-03-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-03-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79618

------------------------------------------------------------------------
r79618 | cevans@chromium.org | Mon Mar 28 14:41:43 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/suid/sandbox.c?r1=79618&r2=79617&pathrev=79618

Landing for Julien Tinnes, jln@google.com:

---
chroot to /proc instead of /tmp. This gets rid of a lot of unnecessary
complexity and fixes a race condition.

(Original idea from Markus)

The chroot helper will chroot to /proc/self/fdinfo (or /proc/self/fd). This is
pretty safe because access to this directory is protected by the ptrace() check
in the kernel and the helper is privileged.

Moreover, as soon as the helper _exit() and becomes a zombie, the directory
will be empty. Zygote should wait() for us to make everything deterministric.

We also export SBX_HELPER_PID so that Zygote can specifically wait for the
helper. 
---

BUG=76542
R=markus,agl
Review URL: http://codereview.chromium.org/6683056
------------------------------------------------------------------------

### sc...@gmail.com (2011-03-28)

Actually, we can merge this to M11 once this rolls successfully into an M12 dev channel release.

### bu...@chromium.org (2011-03-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79867

------------------------------------------------------------------------
r79867 | laforge@chromium.org | Wed Mar 30 11:30:24 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/suid/sandbox.c?r1=79867&r2=79866&pathrev=79867

Revert 79618 - Landing for Julien Tinnes, jln@google.com:

---
chroot to /proc instead of /tmp. This gets rid of a lot of unnecessary
complexity and fixes a race condition.

(Original idea from Markus)

The chroot helper will chroot to /proc/self/fdinfo (or /proc/self/fd). This is
pretty safe because access to this directory is protected by the ptrace() check
in the kernel and the helper is privileged.

Moreover, as soon as the helper _exit() and becomes a zombie, the directory
will be empty. Zygote should wait() for us to make everything deterministric.

We also export SBX_HELPER_PID so that Zygote can specifically wait for the
helper. 
---

BUG=76542
R=markus,agl
Review URL: http://codereview.chromium.org/6683056

TBR=cevans@chromium.org
Review URL: http://codereview.chromium.org/6675053
------------------------------------------------------------------------

### bu...@chromium.org (2011-03-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79869

------------------------------------------------------------------------
r79869 | laforge@chromium.org | Wed Mar 30 11:36:40 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/719/src/sandbox/linux/suid/sandbox.c?r1=79869&r2=79868&pathrev=79869

Revert 79618 - Landing for Julien Tinnes, jln@google.com:

---
chroot to /proc instead of /tmp. This gets rid of a lot of unnecessary
complexity and fixes a race condition.

(Original idea from Markus)

The chroot helper will chroot to /proc/self/fdinfo (or /proc/self/fd). This is
pretty safe because access to this directory is protected by the ptrace() check
in the kernel and the helper is privileged.

Moreover, as soon as the helper _exit() and becomes a zombie, the directory
will be empty. Zygote should wait() for us to make everything deterministric.

We also export SBX_HELPER_PID so that Zygote can specifically wait for the
helper. 
---

BUG=76542
R=markus,agl
Review URL: http://codereview.chromium.org/6683056

TBR=cevans@chromium.org
Review URL: http://codereview.chromium.org/6675054
------------------------------------------------------------------------

### bu...@chromium.org (2011-03-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79921

------------------------------------------------------------------------
r79921 | laforge@chromium.org | Wed Mar 30 16:39:14 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/suid/sandbox.c?r1=79921&r2=79920&pathrev=79921

Revert 79867 - Revert 79618 - Landing for Julien Tinnes, jln@google.com:

---
chroot to /proc instead of /tmp. This gets rid of a lot of unnecessary
complexity and fixes a race condition.

(Original idea from Markus)

The chroot helper will chroot to /proc/self/fdinfo (or /proc/self/fd). This is
pretty safe because access to this directory is protected by the ptrace() check
in the kernel and the helper is privileged.

Moreover, as soon as the helper _exit() and becomes a zombie, the directory
will be empty. Zygote should wait() for us to make everything deterministric.

We also export SBX_HELPER_PID so that Zygote can specifically wait for the
helper. 
---

BUG=76542
R=markus,agl
Review URL: http://codereview.chromium.org/6683056

TBR=cevans@chromium.org
Review URL: http://codereview.chromium.org/6675053

TBR=laforge@chromium.org
Review URL: http://codereview.chromium.org/6780010
------------------------------------------------------------------------

### sc...@gmail.com (2011-03-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-06)

Went out to a dev channel; no fires reported.
Merged to M11: Committed revision 80694.

### bu...@chromium.org (2011-04-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=80694

------------------------------------------------------------------------
r80694 | cevans@chromium.org | Wed Apr 06 14:12:32 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/696/src/sandbox/linux/suid/sandbox.c?r1=80694&r2=80693&pathrev=80694

Merge 79618 - Landing for Julien Tinnes, jln@google.com:---chroot to /proc instead of /tmp. This gets rid of a lot of unnecessarycomplexity and fixes a race condition.(Original idea from Markus)The chroot helper will chroot to /proc/self/fdinfo (or /proc/self/fd). This ispretty safe because access to this directory is protected by the ptrace() checkin the kernel and the helper is privileged.Moreover, as soon as the helper _exit() and becomes a zombie, the directorywill be empty. Zygote should wait() for us to make everything deterministric.We also export SBX_HELPER_PID so that Zygote can specifically wait for thehelper. ---BUG=76542R=markus,aglReview URL: http://codereview.chromium.org/6683056
TBR=cevans@chromium.org
Review URL: http://codereview.chromium.org/6802024
------------------------------------------------------------------------

### sc...@gmail.com (2011-04-14)

@dan.j.rosenberg: thanks for this report! Very interesting. Seems like a stretch to exploit but we're really happy to be without this bug. Accordingly, we'd love to offer a provisional $500 Chromium Security Reward.

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

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-29)

Ok, ping cevans@chromium.org to set up payment :)

### sc...@gmail.com (2011-05-06)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-11-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/76542?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089009)*
