# Security: Local privilege escalation & sandbox escaping via chromeos-6.1 kernel BUG (DirtyVMA)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065952](https://issues.chromium.org/issues/40065952) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | lr...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

DirtyVMA is a vulnerability in the memory management subsystem of the Linux  

kernel. The lock handling for accessing and updating virtual memory areas  

(VMAs) is incorrect, leading to use-after-free problems. This issue can be  

successfully exploited to execute arbitrary kernel code, escalate containers,  

and gain root privileges. The BUG is introduced in conjunction with the  

introduction of the maple tree in kernel v6.1.

This vulnerability was reported upstream a few days ago and the kernel security  

team is working on a fix. The full report and more detailed information about  

this vulnerability can be found in the attachment.

Meanwhile, I have done some experiments and (almost) confirmed that this  

vulnerability can be exploited in the chromeos-6.1 kernel tree [1] under  

the chromeos kernel configs. Since the exploit allows the chronos user  

to gain root privileges and even execute code in kernel context, it  

should be rated as a high severity bug according to the ChromeOS  

Security Severity Guidelines [2].

[1] <https://chromium.googlesource.com/chromiumos/third_party/kernel/+/refs/heads/chromeos-6.1>  

[2] <https://chromium.googlesource.com/chromiumos/docs/+/HEAD/security_severity_guidelines.md>

Note, however, that my experiments at this point were done by booting my  

self-built ChromeOS kernel with QEMU (see the reproduction case below for  

details). This should be sufficient to prove the existence and exploitability  

of this vulnerability. I will later work on a PoC that will fully work in  

ChromeOS Flex, but that may take some time (maybe after the vulnerability has  

already been fixed).

**VERSION**  

Operating System: Linux kernel chromeos-6.1 branch with chromeos kernel configs

**REPRODUCTION CASE**  

Build kernel:  

git clone --branch=chromeos-6.1 --depth 1 <https://chromium.googlesource.com/chromiumos/third_party/kernel.git>  

CHROMEOS\_KERNEL\_FAMILY=chromeos chromeos/scripts/prepareconfig chromiumos-x86\_64  

yes '' | make oldconfig  

make -j16  

Run in QEMU:  

qemu-system-x86\_64 -drive format=raw,file=../disk.ext4,if=ide -kernel arch/x86\_64/boot/bzImage -append "root=/dev/sda init=/bin/sh" -no-reboot -no-shutdown -m 4G -smp 2 -enable-kvm -s  

Run PoC:  

mount -t tmpfs tmp /tmp  

mount -t proc proc /proc  

su guest  

./exp

The PoC source is included, and the way to build this ./exp is simply to use  

./build.sh on top of its source code. It can gain root privileges once the  

kernel function offsets are properly assigned according to the target kernel  

build. Before that, it can only cause kernel panics.

There are also three parameters that may need to be adjusted, depending on the  

specific kernel setup:

First, by default it only works when the number of online CPUs is exactly two.  

If the number of CPUs is greater than 2, the number of objects per maple\_node  

may not be 16. This information can be found in /proc/slabinfo, or it can be  

calculated manually in the same way the kernel does (since slabinfo needs root  

privileges to access it). The OBJS\_PER\_SLAB parameter in node\_master.h must be  

set accordingly.

Second, some timing parameters are also hardcoded. I can provide a simple  

guideline to adjust them here.

1. When you see "use hlt" before "free hlt", it is a "use-before-free"  
   
   case. To make the use happen after the free, increase the  
   
   LONG\_NAME\_FILE\_DEPTH parameter in the long\_file\_name.h so that "use  
   
   hlt" is printed after "free hlt".
2. Then adjust the FREE\_TIMING\_USEC parameter in node\_free.h. If stack  
   
   expansion does not occur when accessing /proc/self/maps  
   
   ("80000-81000" is printed), the parameter needs to be set smaller.  
   
   Otherwise, try making the parameter larger, but if that does not  
   
   work, try making it smaller again. The BUG-triggerable interval  
   
   should be large enough, so a few random tries may help.

**CREDIT INFORMATION**  

Reporter credit: Ruihan Li

DISCLAIMER  

This exploit is also used to participate in the Google kCTF VRP [3]. Roxana Bradescu confirms that multiple Google VRPs do not conflict with each other. At the same time, I'd also like to thank Roxana Bradescu for Roxana's detailed answers to my various questions about ChromeOS VRP.

[3] <https://google.github.io/kctf/>

## Attachments

- [DirtyVMA-upstream.txt](attachments/DirtyVMA-upstream.txt) (text/plain, 10.1 KB)
- [DirtyVMA.tar.xz](attachments/DirtyVMA.tar.xz) (application/octet-stream, 25.8 KB)

## Timeline

### [Deleted User] (2023-06-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-19)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/287898962). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/287898962]

### [Deleted User] (2023-06-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-15)

Upstream Fix complete and verified so will mark as fixed 

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc.."

This is a privileged escalation bug in the new kernel maple tree in kernel 6.1

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

Kernel Memory is exploited here and can be used in sandbox escape.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The fix is coming from upstream. This is a new vuln and it appears the same reporter provided the brief to kernel and chromeos.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

We are not shipping any devices with 6.1 as of the reporting so this highly mitigated.

Severity assessment - why not higher, why not lower

Security Impact None for ChromeOS as we are not yet shipping devices from chromeos-6.1 per https://crbug.com/chromium/1455605#c5

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-06)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### [Deleted User] (2023-11-06)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-22)

This issue was migrated from crbug.com/chromium/1455605?no_tracker_redirect=1

[Monorail blocking: b/287898962]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065952)*
