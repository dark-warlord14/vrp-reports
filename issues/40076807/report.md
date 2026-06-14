# [LangFuzz] Crash at v8::internal::AccessorPair::GetComponent with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40076807](https://issues.chromium.org/issues/40076807) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2013-01-13 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20130104 Firefox/19.0

Steps to reproduce the problem:
1. Run attached javascript in the d8 shell or browser to observe crash (tested on x64 Linux).

What is the expected behavior?

What went wrong?
Crashes with invalid read from dangerous looking address.

Trace from d8:

==8413== Invalid read of size 8
==8413==    at 0x55B9E4: v8::internal::AccessorPair::GetComponent(v8::internal::AccessorComponent) (in /scratch/holler/LangFuzz/v8-3.15/out/x64.release/d8)
==8413==    by 0x5DD051: v8::internal::Runtime_GetOwnProperty(v8::internal::Arguments, v8::internal::Isolate*) (in /scratch/holler/LangFuzz/v8-3.15/out/x64.release/d8)
==8413==    by 0x376B940654D: ???
==8413==    by 0x376B943E89D: ???
==8413==    by 0x376B943C52E: ???
==8413==    by 0x376B943C0BC: ???
==8413==    by 0x376B9430725: ???
==8413==    by 0x376B9425346: ???
==8413==    by 0x376B9412016: ???
==8413==    by 0x46B53D: v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) (in /scratch/holler/LangFuzz/v8-3.15/out/x64.release/d8)
==8413==    by 0x46CECA: v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) (in /scratch/holler/LangFuzz/v8-3.15/out/x64.release/d8)
==8413==    by 0x414F45: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-3.15/out/x64.release/d8)
==8413==  Address 0x13b1e8bb0b80 is not stack'd, malloc'd or (recently) free'd

Trace from browser:

Program received signal SIGSEGV, Segmentation fault.
0x0000555556b8e5d4 in ?? ()
(gdb) bt
#0  0x0000555556b8e5d4 in ?? ()
#1  0x0000555556c32509 in ?? ()
[...]
#14 0x0000000000000000 in ?? ()
(gdb) x /i $pc
=> 0x555556b8e5d4:      mov    0x7(%rdi),%rax
(gdb) info reg rdi
rdi            0x2134163aba29   36507594963497

Did this work before? N/A 

Chrome version: 25.0.1364.29  Channel: dev
OS Version: Ubuntu 12.10

## Attachments

- [crash2013013-AccessorPairGetComponent.js](attachments/crash2013013-AccessorPairGetComponent.js) (text/plain; charset=us-ascii, 352 B)

## Timeline

### in...@chromium.org (2013-01-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-01-13)

[Empty comment from Monorail migration]

### ms...@chromium.org (2013-01-14)

At first I had a hard time reproducing this, as it turns out the repro is x64 only, it runs OOM on ia32 before it has a chance to crash. I'll investigate.

### ms...@chromium.org (2013-01-14)

The problem is an un-handlified reference in a handlified function. The reference is not updated during a GC and causes a random read of the stale reference. Fix is in flight. This is very hard to trigger and I couldn't come up with a reliable repro, I might have to fix this one without a regression test.

### ms...@chromium.org (2013-01-14)

Fixed on V8 bleeding edge and will need to be merged back to M25 only, M24 is unaffected.

http://code.google.com/p/v8/source/detail?r=13367

### de...@googlemail.com (2013-01-14)

What unreliable about the provided test? It crashes for me 100% of the time on x64.

### ms...@chromium.org (2013-01-14)

Yes, the provided test crashes reliably on x64 for me as well. But it turns into an endless loop once the issue is fixed, has a long runtime and is very sensitive to heap layout changes. So IMHO it is not suitable as a regression test by itself.

### in...@chromium.org (2013-01-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-17)

@mstarzinger: thanks! Have you had a chance to merge to M25 yet?

### ms...@chromium.org (2013-01-18)

@scarybeast: We didn't get a Canary that covers the fix so far. But it's on my radar and I will merge to M25 as soon as we have coverage.

### sc...@gmail.com (2013-01-22)

@decoder: thanks, $1000, etc.!

### ms...@chromium.org (2013-01-28)

Merged into the V8 3.15 branch (the version used in Chrome 25) as part of V8 version 3.15.11.13 just now.

https://code.google.com/p/v8/source/detail?r=13524

### sc...@gmail.com (2013-01-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/169723?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076807)*
