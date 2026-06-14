# Crash with PDF at bad IP

| Field | Value |
|-------|-------|
| **Issue ID** | [40051184](https://issues.chromium.org/issues/40051184) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals, Internals>Plugins>PDF |
| **Reporter** | ao...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-11-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening the attached PDF document causes a renderer crash due to bad IP (0x6f00000072).

The repro still needs some more cleaning. I'll take care of the rest in a day or two unless this seems like a duplicate. Filing early because this affects stable, and as this was first found a few weeks ago but I hadn't spotted it among the results, this may well be a duplicate by now.

**VERSION**  

Chrome Version: 17.0.932.0 (affects official stable, beta and unstable)  

Operating System: Linux (Debian 6.0.3, x86\_64)

**REPRODUCTION CASE**  

$ google-chrome rip.pdf  

Tab should open and crash after loading for about 2s.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x0000006f00000072 in ?? ()  

(gdb) bt 5  

#0 0x0000006f00000072 in ?? ()  

#1 0x00007fffe9b89c99 in ?? () from /opt/google/chrome/libpdf.so  

#2 0x00007fffe9ba194b in ?? () from /opt/google/chrome/libpdf.so  

#3 0x00007fffe9bdf58f in ?? () from /opt/google/chrome/libpdf.so  

#4 0x00007fffe9c0f4a9 in ?? () from /opt/google/chrome/libpdf.so  

(More stack frames follow...)  

(gdb) frame 0  

#0 0x0000006f00000072 in ?? ()  

(gdb) i r  

rax 0x6f00000072 476741369970  

rbx 0x7fffffffc080 140737488339072  

rcx 0x7fffffffc0c0 140737488339136  

rdx 0x7fffe704b000 140737069232128  

rsi 0x200 512  

rdi 0x7fffe704b000 140737069232128  

rbp 0x7fffffffc110 0x7fffffffc110  

rsp 0x7fffffffbeb8 0x7fffffffbeb8  

r8 0x7fffffffc110 140737488339216  

r9 0x101010101010101 72340172838076673  

r10 0x200 512  

r11 0x7fffee8fb38c 140737195783052  

r12 0x7fffffffbfe0 140737488338912  

r13 0x7ffff862bd80 140737360608640  

r14 0x7fffe6f04a60 140737067895392  

r15 0x7fffffffc0c0 140737488339136  

rip 0x6f00000072 0x6f00000072  

eflags 0x10206 [ PF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

This didn't reproduce under Valgrind here.

## Attachments

- deleted (application/octet-stream, 0 B)
- [rip-2.pdf](attachments/rip-2.pdf) (application/pdf; charset=us-ascii, 19.9 KB)

## Timeline

### sc...@gmail.com (2011-11-13)

Ooh! A task for Monday.

### ao...@gmail.com (2011-11-14)

Down to 121 lines of ASCII. I need to do some other stuff and flush my wtf-buffer before continuing.

### ao...@gmail.com (2011-11-14)

Weird bug. A few notes in case they might help: The original sample was a malware PDF which had a few compressed streams, one of which was JS which under some obfuscation built the actual exploit string and passed it to eval as usual. Here however the crash comes while building the payload. This phase reads words from the pages, takes chars, does a fixed xor on them and then appends the results to a string. Instead of anything sensible (to me) the crash depends on silly features like placement of semicolons and the in which strings are built and functions are called.

The IP seems to come from an indirect jump via rax a few branches before the crash, and the address might be related to ascii values of o and r.

### sc...@gmail.com (2011-11-14)

What is this Aki, month of Heisenbugs? :P

This doesn't fire under debug. Grrr!! I definitely reproduce it in an optimized build. Any idea if it affects 32-bit? I've seen some 64-bit-only bugs with similar traits......

### ao...@gmail.com (2011-11-14)

@scarybeasts Doesn't reproduce on 32-bit using any of my repros. Good thing at least GDB gets this :)

### sc...@gmail.com (2011-11-14)

If this is in the garbage collector again, I may have to become upset.

### sc...@gmail.com (2011-11-14)

It's definitely a corrupt vtable, so assigning severity appropriately.
My dark suspicion at this time is that it _is_ a garbage collector-based use-after-free. These are awful to debug, accordingly a $500 Chromium Security Fine :P

### sc...@gmail.com (2011-11-14)

I forgot the label.

### sc...@gmail.com (2011-11-15)

Ok, I think I have this but it was a sufficient headache that I'm doubling the fine :P

Some notes on why it's so hard to debug:
- It's sensitive to object sizes (allocation slabs etc). so debug vs. opt and 32 vs. 64-bit affects reproducability.
- Garbage collection needs to trigger at _exactly_ the right (or wrong?) time so any changes to allocations basically breaks the repro. Regrettably, my fix changes around allocation strategy so it's hard to be sure it's really fixed, other than the fact I understand why the bug happens.
- The root cause is that object copies are taken for the passed arguments when internal functions are called. These copies are allocated from the garbage-managed pool, but unfortunately no rooted object holds a direct pointer to the copies. So for a very brief window of opportunity, the garbage collector considers itself at liberty to blow away these temporary objects.

### ao...@gmail.com (2011-11-15)

Ouch, sorry to ruin your Monday. GC bugs are indeed interesting times. Some have ruined a lot more than one day for me :)

### sc...@gmail.com (2011-11-15)

The fix, which I hope to land shortly, is complicated. I don't feel particularly disposed to merge it to M16. Given the tricky preconditions, I think we can wait until M17 for this fix.

### sc...@gmail.com (2011-11-16)

Fixed at PDF r1162
Compile checked on Windows
DEPS rolled on trunk at PDF r1163

### sc...@gmail.com (2011-11-17)

Thanks for an interesting bug, Aki. The test case is realistically unreducable because the slightest change in order of allocations etc. will throw off the timing of the garbage collect. Hence, a $1000 Chromium Security Reward!

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

### ao...@gmail.com (2011-11-17)

Talk about mixed messages.. Thanks :)

### sc...@gmail.com (2011-12-20)

Payment in system.
Looks like this one got paid early -- oops, oh well :)

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/104056?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051184)*
