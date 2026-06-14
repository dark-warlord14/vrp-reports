# Crash at NULL IP in PDF when evaluating strange expression

| Field | Value |
|-------|-------|
| **Issue ID** | [40084783](https://issues.chromium.org/issues/40084783) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-11-10 |
| **Bounty** | $1,000.00 |

## Description

Filing on behalf of Aki. Original repro is attached.

Details provided by Aki over personal e-mail:
Program received signal SIGSEGV, Segmentation fault.
0x0000000000000000 in ?? ()
(gdb) bt
#0  0x0000000000000000 in ?? ()
#1  0x00007fffec5c26e3 in ?? () from /opt/google/chrome/libpdf.so
#2  0x00007fffec5d1edf in ?? () from /opt/google/chrome/libpdf.so
#3  0x00007fffec5b6370 in ?? () from /opt/google/chrome/libpdf.so
[...]
(gdb) frame 1
#1  0x00007fffec5c26e3 in ?? () from /opt/google/chrome/libpdf.so
(gdb) disas $rip-32, $rip+8
Dump of assembler code from 0x7fffec5c26c3 to 0x7fffec5c26eb:
  0x00007fffec5c26c3:  sub    $0x38,%esp
  0x00007fffec5c26c6:  cmpq   $0x0,0x8(%rdi)
  0x00007fffec5c26cb:  mov    %rsi,%r12
  0x00007fffec5c26ce:  mov    %rdx,%rbp
  0x00007fffec5c26d1:  je     0x7fffec5c2702
  0x00007fffec5c26d3:  mov    0x8(%rbx),%rdi
  0x00007fffec5c26d7:  mov    %rbp,%rdx
  0x00007fffec5c26da:  mov    %r12,%rsi
  0x00007fffec5c26dd:  mov    (%rdi),%rax
  0x00007fffec5c26e0:  callq  *0x78(%rax)
=> 0x00007fffec5c26e3:  test   %rax,%rax
  0x00007fffec5c26e6:  mov    %rax,%rbx
  0x00007fffec5c26e9:  je     0x7fffec5c2715

## Attachments

- [nullip.pdf](attachments/nullip.pdf) (application/pdf; charset=binary, 61.1 KB)

## Timeline

### sc...@gmail.com (2010-11-10)

Simplified repro: http://scary.beasts.org/misc/pdfjs.html?js=app.alert(1+function(){})

Or http://scary.beasts.org/misc/c.pdf, put 1+function(){} in text field then hit button.

### sc...@gmail.com (2010-11-10)

There are also functional crazinesses to this bug. Before my upcoming fix, the following JS returns 'undefined' instead of '7'.

a=function(){return 7;};app.alert(a());

### sc...@gmail.com (2010-11-10)

@aohelin: another nice and interesting bug, $1000, etc. :D

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

### ao...@gmail.com (2010-11-10)

Excellent \o/

### sc...@gmail.com (2010-11-10)

Fixed on trunk (r683), merged to M8 (r685). Should make this week's Beta, thanks Aki.

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: More fuzzy classification of security bugs not affecting stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/62623?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084783)*
