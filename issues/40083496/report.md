# Crash in PDF plugin when building cross-refs

| Field | Value |
|-------|-------|
| **Issue ID** | [40083496](https://issues.chromium.org/issues/40083496) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Plugins>PDF |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-10-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Memory corruption with malformed PDF. Due to an off-by-one access when rebuilding cross-refs?  

Splitting out from <https://crbug.com/chromium/56760> on behalf of Aki Helin.

Errant PDF is attached.

Debug details provided by Aki as follows:  

crash-11:14:44.pdf segv is at crash dump id: 99829e3c9b4b07d4.

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xb7c52b70 (LWP 22357)]  

0x0874b98b in ?? ()  

(gdb) bt  

#0 0x0874b98b in ?? ()  

#1 0x0874bcf0 in ?? ()  

#2 0x0a9084e1 in operator delete(void\*) ()  

#3 0x087696bc in ?? ()  

#4 0x087697d6 in ?? ()  

#5 0x08769e9a in ?? ()  

#6 0x087919c0 in ?? ()  

#7 0x0876a204 in ?? ()  

#8 0x0876a306 in ?? ()  

#9 0x08783380 in ?? ()  

#10 0x087752c1 in ?? ()  

#11 0x00a6796e in start\_thread (arg=0xb7c52b70) at pthread\_create.c:300  

#12 0x00fdca4e in clone () at ../sysdeps/unix/sysv/linux/i386/clone.S:130  

(gdb) info registers  

eax 0x18c 396  

ecx 0xc 12  

edx 0x5 5  

ebx 0xab89fe0 179871712  

esp 0xb7c51fd0 0xb7c51fd0  

ebp 0xb7c52008 0xb7c52008  

esi 0xa9de334 178119476  

edi 0xa9de334 178119476  

eip 0x874b98b 0x874b98b  

eflags 0x210206 [ PF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

(gdb) disas $eip-25, $eip+32  

Dump of assembler code from 0x874b972 to 0x874b9ab:  

0x0874b972: xor %ebx,%ebx  

0x0874b974: test %ecx,%ecx  

0x0874b976: je 0x874b99d  

0x0874b978: mov (%edi),%ebx  

0x0874b97a: cmp $0x1,%ecx  

0x0874b97d: mov %ebx,%edx  

0x0874b97f: jle 0x874b993  

0x0874b981: mov %ebx,%eax  

0x0874b983: mov $0x1,%edx  

0x0874b988: add $0x1,%edx  

=> 0x0874b98b: mov (%eax),%eax  

0x0874b98d: cmp %ecx,%edx  

0x0874b98f: jne 0x874b988  

0x0874b991: mov %eax,%edx  

0x0874b993: mov (%edx),%eax  

0x0874b995: mov %eax,(%edi)  

0x0874b997: movl $0x0,(%edx)  

0x0874b99d: movzwl 0x4(%edi),%eax  

0x0874b9a1: sub %cx,%ax  

0x0874b9a4: cmp 0x6(%edi),%ax  

0x0874b9a8: mov %ax,0x4(%edi)  

End of assembler dump.

Moving straight to Fixed because this is committed to the latest internal PDF branch. It'll take a little while to make canary / dev.

## Attachments

- [crash-11:14:44.pdf](attachments/crash-11_14_44.pdf) (application/pdf; charset=binary, 18.1 KB)

## Timeline

### sc...@gmail.com (2010-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-15)

Aki -- might be worth a quick verification on the latest dev channel? Hopefully this fix made it in.

Root cause here was an off-by-one. Nice bug.

### ao...@gmail.com (2010-10-15)

No crash in 62249, being the current google-chrome-unstable in Ubuntu. Happy tab.

### sc...@gmail.com (2010-10-15)

Those tabs are all having a party! :D

### sc...@gmail.com (2010-10-15)

@aohelin: congratulations! This report qualifies for a provisional $500 Chromium Security Reward. Going with the base level on this one because I extracted this separate issue from https://crbug.com/chromium/56760.

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

### ao...@gmail.com (2010-10-16)

Most excellent :)

Thanks for spotting the different crash in the first place. This bounty, if it gets less provisional, should go to Red Cross. 

### sc...@gmail.com (2010-10-18)

Thank you Aki. $1337 is being sent along to Red Cross.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: More fuzzy classification of security bugs not affecting stable.

### sc...@gmail.com (2012-07-09)

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

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/57501?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083496)*
