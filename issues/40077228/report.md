# [LangFuzz] Crash on Heap with invalid read (possibly due to uninitialized value) on 64 bit

| Field | Value |
|-------|-------|
| **Issue ID** | [40077228](https://issues.chromium.org/issues/40077228) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2013-03-18 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:21.0) Gecko/20130314 Firefox/21.0

Steps to reproduce the problem:
1. Run the following JS code:

var a = [ false ];
for (var i in a) {}
while (a.length < (2 << 11)) { a+= 'x'; }
for (var apply = 0; i < 10; i++) {
  for (var j = 0; j < 10; j++) {
    a.replace(/^(.*)/, encodeURI);
  }
  a += a;
}

2. Observe crash

What is the expected behavior?

What went wrong?
Tab crashes, crash trace:

Program received signal SIGSEGV, Segmentation fault.
0x00003e1c9ba17937 in ?? ()
(gdb) bt
#0  0x00003e1c9ba17937 in ?? ()
[... no symbols available ...]
(gdb) x /i $pc
=> 0x3e1c9ba17937:      cmpb   $0x80,0xb(%rdx)
(gdb) info reg rdx
rdx            0x40b7e1bb4801a8ff       4663444133648640255

I also tried a d8 debug build but it does not crash. In the d8 optimized build I see use of uninitialized value before the crash, so this might be related.

Did this work before? N/A 

Chrome version: 27.0.1438.7 (Official Build 187670) dev  Channel: dev
OS Version: Ubuntu 12.04

## Timeline

### de...@googlemail.com (2013-03-18)

I have a second issue (crash with SIGILL) but the bug tracker doesn't let me open any bugs, I'm always getting 400 Bad Request. Let me know when it's fixed so I can report. It could also be related to this issue.

### js...@chromium.org (2013-03-18)

Forwarding to v8 team for triage.

### da...@chromium.org (2013-03-19)

Looks suspiciously related to the encodeURI work that Yang did a while back, especially the cmpb, which could be a string instance type check?

### ya...@chromium.org (2013-03-19)

I was able to bisect this to https://chromiumcodereview.appspot.com/12263031/ (Enable weak embedded maps in optimized code by default.). Running the same test with --noweak-embedded-maps-in-optimized-code prevents the crash.

### de...@googlemail.com (2013-03-19)

I confirmed that the other test also doesn't crash/sigill anymore with --noweak-embedded-maps-in-optimized-code. The test is this:

var re = /^(?=a)/;
for (;;) {
  re[re] = function() {};
} 


I assume it's the same or a very similar failure then.

### ul...@chromium.org (2013-03-19)

Thanks for bisecting, Yang. I am looking into it.

### ya...@chromium.org (2013-03-19)

We found out what was the issue. In the second test case, the following happens:

- at some point, the toString function is optimized
- and from there, we call into the StringAddStub
- StringAddStub causes a GC, including mark compact
- mark compact collects maps on which the optimized toString depends
- toString is forcibly deoptimized. It is still on the stack, so right after the call to StringAddStub, the code should be patched with a deopt sequence
- except that it's not. Some other calls have been patched, however.
- when we return to the deoptimized toString function, we continue executing a dozen of more instructions, as the code after the call has not been patched
- in that unpatched code, we arrive at a jump, which jumps into the middle of the deopt sequence after another call, which has been correctly patched
- executing the middle of the deopt sequence leads to SIGILL

The reason is that we have not marked HStringAdd as SetAllSideEffects, so that we don't insert a simulate after HStringAdd. Under the assumption that it can cause GC, but no side effects, that's alright. But now that GC can cause deopts, there is a side effect.

Adding a simulate after HStringAdd solves the issue.

For now maybe we should disable the --weak-embedded-maps-in-optimized-code flag so that GC doesn't cause deopts.

### ya...@chromium.org (2013-03-19)

Even though the repros are limited to x64, this issue potentially affects all platforms.

### pa...@chromium.org (2013-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### ya...@chromium.org (2013-03-27)

Test case has been added to V8, flag causing this crash has been disabled for the time being.

### sc...@gmail.com (2013-03-27)

Thank you @yangguo! Excited about the test, the bug shouldn't come back :-)

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-03)

Thanks decoder! $1000

### pa...@chromium.org (2013-05-28)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/217858?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077228)*
