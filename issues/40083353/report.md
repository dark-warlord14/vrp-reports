# segfault in bundled pdf viewer

| Field | Value |
|-------|-------|
| **Issue ID** | [40083353](https://issues.chromium.org/issues/40083353) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2010-09-24 |
| **Bounty** | $1,000.00 |

## Description

Viewing the attached PDF file causes a renderer process segmentation fault in Google Chrome 7.0.517.13 (Official Build 60244) dev on Ubuntu 10.04 (x86 and x86_64).

The error occures when reading ecx having value 0 on both x86 and x86_64, so at least locally just a null deref. In previous version this also crashed, but would not reproduce within gdb, which was odd. Hard to say anything about severity without debugging symbols, and the non-reproducibility in gdb could hint trouble in the stack, so reporting as a security issue to be on the safe side.

I'll run minimization on the file later in case this does not seem to be a duplicate. 

Program received signal SIGSEGV, Segmentation fault.
0x0156a405 in ?? () from /opt/google/chrome/libpdf.so
(gdb) bt
#0  0x0156a405 in ?? () from /opt/google/chrome/libpdf.so
#1  0x0156a849 in ?? () from /opt/google/chrome/libpdf.so
#2  0x0155f49a in ?? () from /opt/google/chrome/libpdf.so
#3  0x0155ed0c in ?? () from /opt/google/chrome/libpdf.so
#4  0x08d56d06 in ?? ()
[...]
(gdb) info registers
eax            0xaac4000        179060736
ecx            0x0      0
edx            0x0      0
ebx            0x18fffec        26214380
esp            0xbfffdf40       0xbfffdf40
ebp            0xbfffe008       0xbfffe008
esi            0xaa8de90        178839184
edi            0x0      0
eip            0x156a405        0x156a405
eflags         0x210246 [ PF ZF IF RF ID ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51
(gdb) disas $eip-32, $eip+32
Dump of assembler code from 0x156a3e5 to 0x156a425:
   0x0156a3e5:  cmp    %edx,-0x90(%ebp)
   0x0156a3eb:  je     0x156a63d
   0x0156a3f1:  mov    -0x90(%ebp),%edi
   0x0156a3f7:  mov    0x8(%ebp),%eax
   0x0156a3fa:  shl    $0x4,%edi
   0x0156a3fd:  mov    %edi,%ecx
   0x0156a3ff:  mov    0xc(%eax),%edx
   0x0156a402:  add    -0x2c(%ebp),%ecx
=> 0x0156a405:  sub    0x8(%ecx),%edx
   0x0156a408:  mov    %edx,%eax
   0x0156a40a:  shr    $0x1f,%eax
   0x0156a40d:  add    %edx,%eax
   0x0156a40f:  sar    %eax
   0x0156a411:  mov    %eax,(%ecx)
   0x0156a413:  cmpb   $0x0,-0x9d(%ebp)
   0x0156a41a:  jne    0x156a3a6
   0x0156a41c:  mov    0x8(%ebp),%eax
   0x0156a41f:  mov    -0x90(%ebp),%edx
End of assembler dump.


## Attachments

- [segv-ecx.pdf](attachments/segv-ecx.pdf) (application/pdf; charset=binary, 87.1 KB)
- [pdf-test.sh](attachments/pdf-test.sh) (text/x-shellscript; charset=us-ascii, 612 B)
- [pdfs.tar.gz](attachments/pdfs.tar.gz) (application/x-gzip; charset=binary, 115.6 KB)
- [malloc.pdf](attachments/malloc.pdf) (application/pdf; charset=binary, 53.3 KB)

## Timeline

### sc...@gmail.com (2010-09-24)

Thanks Aki. I'll take a look soon.

### sc...@gmail.com (2010-09-27)

Hmm. I can't reproduce (yet) reproduce with my local latest PDF code. I'm going to look into a few more things though.

Can you attach the original non-corrupt PDF? I want to see if it is using any interesting features such as passwords, forms, etc.


### sc...@gmail.com (2010-09-27)

Interesting. Reproduces a sad tab in Windows canary build 7.0.530.0
WinDbg seems to indicate some form of process death I don't understand -- like it's dying as the result of a system call?

jam@, would you mind taking a quick look with a fully debuggable stack?

### ao...@gmail.com (2010-09-27)

The original seems to be from http://lomake.fi/forms/pdf/STM/6.02/fi. A quick comparison (hexdump -e '1 1 "%02x\n"' + diff) shows lots of silly changes.. I'll try to find/come up with a better file to trigger this.

### ao...@gmail.com (2010-09-27)

I tried making simpler files triggering this issue by writing a quick and dirty script to fuzz just the above mentioned file. I'm guessing this issue has a memory corruption/stack issue/something causing it to manifest in many ways, because in the first roughly half an hour of running the script found 7 crashes with 4 unique eip and address combinations, which seems a bit fishy.

Added the first few crashing files and the test script, in case you want to have a look. All reproduce with 0 or more reloads on my Ubuntu x86 machine with current google-chrome-unstable.

Will try to minimize the triggering file later with some other approach.

### ao...@gmail.com (2010-09-27)

I left the script running for a while, and it looks like there are two issues. The original segv-ecx.pdf and other similar files seem to cause a segfault on first load reading address 8, and another class of files crash with 50% probability at varying places in code and memory, usually at address below 200, and often show malloc in stack trace. Added one such file here. Reloading it on my machine looks like:

Sep 27 18:08:13 play kernel: [215572.468461] chrome[22030]: segfault at 18b ip 0874c32f sp bfebf5e0 error 4 in chrome[8048000+289a000]
Sep 27 18:08:15 play kernel: [215574.569835] chrome[22035]: segfault at 153 ip 0874c32f sp bfebf250 error 4 in chrome[8048000+289a000]
Sep 27 18:08:18 play kernel: [215577.635874] chrome[22042]: segfault at 18c ip 0874c32f sp bfebf5e0 error 4 in chrome[8048000+289a000]
Sep 27 18:08:20 play kernel: [215579.623653] chrome[22047]: segfault at 18c ip 0874c32f sp bfebf250 error 4 in chrome[8048000+289a000]
Sep 27 18:08:22 play kernel: [215581.477988] chrome[22054]: segfault at 200a00be ip 0874cf5b sp b7369fd0 error 4 in chrome[8048000+289a000]
Sep 27 18:08:24 play kernel: [215582.779745] chrome[22057]: segfault at 200a00be ip 08750146 sp bfebf490 error 4 in chrome[8048000+289a000]
Sep 27 18:08:25 play kernel: [215584.383093] chrome[22060]: segfault at 18c ip 0874c32f sp bfebf250 error 4 in chrome[8048000+289a000]
Sep 27 18:08:27 play kernel: [215585.678198] chrome[22065]: segfault at 18a ip 0874c32f sp bfebf4e0 error 4 in chrome[8048000+289a000]
Sep 27 18:08:28 play kernel: [215586.711530] chrome[22070]: segfault at 18c ip 08750146 sp bfebf430 error 4 in chrome[8048000+289a000]
Sep 27 18:08:29 play kernel: [215588.245062] chrome[22073]: segfault at ffc64edb ip 0874c32f sp bfebf250 error 4 in chrome[8048000+289a000]
Sep 27 18:08:30 play kernel: [215589.139165] chrome[22078]: segfault at faa0b98d ip 08d22dc0 sp bfebfed0 error 5 in chrome[8048000+289a000]
Sep 27 18:08:31 play kernel: [215590.613599] chrome[22083]: segfault at 18b ip 0874c32f sp bfebf5e0 error 4 in chrome[8048000+289a000]

Looks like a possibly separate memory corruption/use after free issue, but leaving it up to you.

### sc...@gmail.com (2010-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-27)

malloc.pdf and most of pdfs.tar.gz give me "Mismatched free() / delete / delete []" in valgrind. That seems to be a duplicate of a couple of conditions I sent to the PDF team a week back. (Can attach demo files ufuzz51.pdf, ufuzz1.pdf on request).

crash-11:14:44.pdf seems different. I see an "Invalid read of size 4" seemingly related to rebuilding corrupt cross-refs. I'll retry all these files once I get an update build of the latest PDF to code to play with.

### sc...@gmail.com (2010-09-30)

Let's use this bug to track segv-ecx.pdf. There does seem to be some out-of-bounds memory corruption going on with that file. It's being investigated by our PDF team.

The "Mismatched free() / delete / delete []" was previously known and is fixed in our latest internal build.

There still might be something new with crash-11:14:44.pdf. I don't get a crash but I do see an invalid read in valgrind. If you do get a real SEGV with this file, could you send over registers at crash + crash location + faulting instruction + etc? We can fork it off to a separate bug if it is significant :)

### sc...@gmail.com (2010-09-30)

[Empty comment from Monorail migration]

### ao...@gmail.com (2010-09-30)

crash-11:14:44.pdf segv is at crash dump id: 99829e3c9b4b07d4.

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb7c52b70 (LWP 22357)]
0x0874b98b in ?? ()
(gdb) bt
#0  0x0874b98b in ?? ()
#1  0x0874bcf0 in ?? ()
#2  0x0a9084e1 in operator delete(void*) ()
#3  0x087696bc in ?? ()
#4  0x087697d6 in ?? ()
#5  0x08769e9a in ?? ()
#6  0x087919c0 in ?? ()
#7  0x0876a204 in ?? ()
#8  0x0876a306 in ?? ()
#9  0x08783380 in ?? ()
#10 0x087752c1 in ?? ()
#11 0x00a6796e in start_thread (arg=0xb7c52b70) at pthread_create.c:300
#12 0x00fdca4e in clone () at ../sysdeps/unix/sysv/linux/i386/clone.S:130
(gdb) info registers
eax            0x18c    396
ecx            0xc      12
edx            0x5      5
ebx            0xab89fe0        179871712
esp            0xb7c51fd0       0xb7c51fd0
ebp            0xb7c52008       0xb7c52008
esi            0xa9de334        178119476
edi            0xa9de334        178119476
eip            0x874b98b        0x874b98b
eflags         0x210206 [ PF IF RF ID ]
cs             0x73     115
ss             0x7b     123
ds             0x7b     123
es             0x7b     123
fs             0x0      0
gs             0x33     51

(gdb) disas $eip-25, $eip+32
Dump of assembler code from 0x874b972 to 0x874b9ab:
   0x0874b972:  xor    %ebx,%ebx
   0x0874b974:  test   %ecx,%ecx
   0x0874b976:  je     0x874b99d
   0x0874b978:  mov    (%edi),%ebx
   0x0874b97a:  cmp    $0x1,%ecx
   0x0874b97d:  mov    %ebx,%edx
   0x0874b97f:  jle    0x874b993
   0x0874b981:  mov    %ebx,%eax
   0x0874b983:  mov    $0x1,%edx
   0x0874b988:  add    $0x1,%edx
=> 0x0874b98b:  mov    (%eax),%eax
   0x0874b98d:  cmp    %ecx,%edx
   0x0874b98f:  jne    0x874b988
   0x0874b991:  mov    %eax,%edx
   0x0874b993:  mov    (%edx),%eax
   0x0874b995:  mov    %eax,(%edi)
   0x0874b997:  movl   $0x0,(%edx)
   0x0874b99d:  movzwl 0x4(%edi),%eax
   0x0874b9a1:  sub    %cx,%ax
   0x0874b9a4:  cmp    0x6(%edi),%ax
   0x0874b9a8:  mov    %ax,0x4(%edi)
End of assembler dump.


### sc...@gmail.com (2010-09-30)

Eww, crash in the allocator on https://crbug.com/chromium/56760#c11. Let me see about when our latest PDF code will get pushed to canary (and/or dev) to see if this is a new one or not.

### sc...@gmail.com (2010-10-01)

crash-11:14:44.pdf split off into http://code.google.com/p/chromium/issues/detail?id=57501

### sc...@gmail.com (2010-10-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2010-10-05)

[Empty comment from Monorail migration]

### ke...@chromium.org (2010-10-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-13)

Heya John, did we get resolution on this one?

### ja...@chromium.org (2010-10-14)

yep, it's fixed.

### sc...@gmail.com (2010-10-14)

@aohelin: apparently, this one is resolved on our internal build. I'm not sure if it made it into the latest dev channel or not. Does is still repro? Tentatively marking as fixed.

### ao...@gmail.com (2010-10-14)

No crash in 8.0.552.0 (Official Build 62249) dev, being current google-chrome-unstable in Ubuntu. Tab remains happy.

### sc...@gmail.com (2010-10-15)

Thanks for the verification! We did confirm the that root cause is an out-of-bounds write so I will convene the panel :)

### sc...@gmail.com (2010-10-15)

@aohelin: congratulations! This provisionally qualifies for a $1000 Chromium Security Reward. We're rewarding above the base level thanks to the quality of report: good repros, good analysis and general helpfulness.

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

Excellent \o/

### sc...@gmail.com (2010-10-27)

Payment is in the electronic system.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-03)

[Empty comment from Monorail migration]

### ja...@gmail.com (2010-11-22)

Hey,

I wanted to use "malloc.pdf" for fuzzing, but I've seen that it still crashes on Windows XP SP3. Sorry but i cannot get a stacktrace for it.

Checked:

Chrome stable 7.0.517.44 -> Crash
Chrome dev 9.0.587.0 dev -> Not crash

Any idea? Maybe other issue?

Thanks,
Jose.

### ao...@gmail.com (2010-11-22)

Malloc.pdf looks like the crash in issue #62175. A stack exhaustion is causing crashes in a few different places, one of which is this one happening in malloc. In all cases it seems to be harmless and comes from stack operations, like pushing ebp in this one.

### ja...@gmail.com (2010-11-23)

Thanks for the clarification :)

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: fuzzily determined that this security bug did not affect a stable release.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/56760?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083353)*
