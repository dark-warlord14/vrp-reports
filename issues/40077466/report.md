# [LangFuzz] Crash on heap with invalid read on dangerous (possibly uninitialized) address (64 bit)

| Field | Value |
|-------|-------|
| **Issue ID** | [40077466](https://issues.chromium.org/issues/40077466) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2013-04-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20130413 Firefox/22.0

Steps to reproduce the problem:
1. Run the following JS code in the browser or d8 shell:

var new_space_string = "";
for (var i = 0; i < 12800; ++i) {
  new_space_string += String.fromCharCode(Math.random() * 26 + (4294967295) | 0);
}

2. Observe crash.

What is the expected behavior?
No Crash.

What went wrong?
Browser tab crashes:

Program received signal SIGSEGV, Segmentation fault.
0x000038c93d3504ce in ?? ()
(gdb) bt
#0  0x000038c93d3504ce in ?? ()
[...]
#16 0x0000000000000000 in ?? ()
(gdb) x /i $pc
=> 0x38c93d3504ce:      mov    0xf(%rbx,%rax,8),%rbx
(gdb) info reg rbx rax
rbx            0x3d698c9051f1   67523539128817
rax            0x100000004      4294967300

Valgrind trace for d8:

==24262== Invalid read of size 8
==24262==    at 0x30D219A34988: ???
==24262==    by 0x30D219A25D03: ???
==24262==    by 0x30D219A0C336: ???
==24262==    by 0x46F24E: v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) (in v8-trunk/out/x64.release/d8)
==24262==    by 0x47098C: v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) (in v8-trunk/out/x64.release/d8)
==24262==    by 0x414FBC: v8::Script::Run() (in v8-trunk/out/x64.release/d8)
==24262==    by 0x406628: v8::Shell::ExecuteString(v8::Isolate*, v8::Handle<v8::String>, v8::Handle<v8::Value>, bool, bool) (in v8-trunk/out/x64.release/d8)
==24262==    by 0x4082CA: v8::SourceGroup::Execute(v8::Isolate*) (in v8-trunk/out/x64.release/d8)
==24262==    by 0x409019: v8::Shell::RunMain(v8::Isolate*, int, char**) (in v8-trunk/out/x64.release/d8)
==24262==    by 0x409850: v8::Shell::Main(int, char**) (in v8-trunk/out/x64.release/d8)
==24262==    by 0x580BEEC: (below main) (in /lib64/libc-2.12.2.so)
==24262==  Address 0x128275505218 is not stack'd, malloc'd or (recently) free'd

Did this work before? N/A 

Chrome version: 28.0.1485.0  Channel: dev
OS Version: Ubuntu 12.10

The crash address keeps changing even in the shell, I assume this could be another uninitialized pointer or something similar.

## Timeline

### in...@chromium.org (2013-04-25)

[Empty comment from Monorail migration]

### da...@chromium.org (2013-04-27)

As always, nice catch decoder. Thanks. This is a problem with StringCharFromCode on x64 only. We untag a SMI into rax, and then check with a cmpl that the bottom 32-bits are a valid index into a lookup table. Unfortunately, we use rax directly in an indexed addressed movq, in which the top 32-bits are garbage and the index multiplication therefore ends up in an effective address way beyond the end of the table. So, a carefully crafted exploit would read memory at increments of 4GB in blocks that are the size of the lookup table. Not sure how interesting that is to exploit.

Fix is easy, just movsxlq rax before the indexed load. I've got a patch in review and it will be in our next roll.

### sc...@gmail.com (2013-04-27)

[Empty comment from Monorail migration]

### da...@chromium.org (2013-04-29)

Fixed in V8 bleeding_edge r14481.

### in...@chromium.org (2013-04-29)

Danno@, was this a recent regression. Which branches are affected ?

### da...@chromium.org (2013-04-30)

M26 and M27 are both affected, so we will need to merge back to both once we get sufficient Canary coverage.

### in...@chromium.org (2013-04-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-03)

Thanks decoder! $500

Danno, we only need to merge to M27 now I think. Has this been taken care of?

### da...@chromium.org (2013-05-03)

I haven't merged yet, I'll do it Monday first thing... I was waiting to get some Canary coverage before merging back, but I think we have that now.

### da...@chromium.org (2013-05-06)

I merged the fix back to M27.

### sc...@gmail.com (2013-05-06)

Thanks Danno!

### sc...@gmail.com (2013-05-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### cl...@chromium.org (2016-02-02)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/235311?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077466)*
