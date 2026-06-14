# v8 fuzzing - 1108 potential use-after-free in RegExp code

| Field | Value |
|-------|-------|
| **Issue ID** | [40088408](https://issues.chromium.org/issues/40088408) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-03-02 |
| **Bounty** | $1,000.00 |

## Description

Upstream http://code.google.com/p/v8/issues/detail?id=1108

Lasse:
The RegExpExecStub is used to call generated RegExp code from JS code.
RegExp code is generally treated as C-code in its calling convention (it has no JS stack-frames, and can call directly to C functions in some cases, like stack overflow). 
Normally when we call C code from JS code, we use a specific C entry protocol that sets up the stack and (global) C variables correctly. However, the RegExpExecStub didn't do this, and just called the RegExp code.
That means that some C-level variables were not set up correctly, and if the RegExp code called out to C code, it would be in an incorrect state.
The state that wasn't set correctly was Top::c_entry_fp_address and Top::context_address.
The c_entry_fp_address is a link to the last JS frame on the JS stack. It's used to traverse the JS stack by C code.
The context_address points to the current JS context. It's probably not changing much in the same thread.

When returning (properly) from C code, we always clear the k_c_entry_fp_address, but only clear the context address in debug mode (MacroAssembler::LeaveExitFrameEpilogue).
If we reenter JS from C code, we don't clear either (JSEntryStub::GenerateBody).

If I'm not missing anything, it means that a calling sequence of C -> JS -> C -> JS -> RegExp -> C could leave the c_entry_fp_address as the one set by the first JS->C call, which means that stack traversal during the final C call will skip the second JS call's stack frames. Maybe that can cause some JS-heap objects to be GC'ed during the C call, because the stack frames aren't traversed for GC roots, leaving the pointers of that stack potentially dangling.
The unhandled pointers on the stack will still point to V8 Heap memory - potentially to the old-semispace of new-space, or into the middle of other objects in a compacted old-space. If an attacked finds a way to predict GCs with uncanny precission, and makes such a pointer suddently point into the middle of a specially crafted string, he might be able to use that to read arbitrary memory, because the middle of a string can look like the header of a very long flat string object where you can read individual 16-bit values using String.prototype.charCodeAt. it may even be possible to write arbitrary memory, if you can make the data look like a long JS Array.

I think it'll be incredibly hard to pull off, but I can't say that it's impossible (that's why we need real security people, not just paranoid engineers!)

## Timeline

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-02)

Sounds more like a medium severity due to the complexity, but @skylined feel free to bump it back up if you disagree.

### sc...@gmail.com (2011-03-03)

Does not appear to affect M9

### sc...@gmail.com (2011-03-03)

Actually does affect M9; the repro in 1148
http://code.google.com/p/v8/issues/detail?id=1148
Does fire (1148 was marked as a dup of 1108)

### sc...@gmail.com (2011-03-03)

Putting back up to high; it manifests pretty awfully in M9:


Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
(gdb) bt
#0  0x00000000 in ?? ()
#1  0x08b2b604 in ?? ()
#2  0xb6afc25d in ?? ()

Or


Program received signal SIGILL, Illegal instruction.
0x00200001 in ?? () from /opt/google/chrome/libsmime3.so.1d

#0  0x00200001 in ?? () from /opt/google/chrome/libsmime3.so.1d
#1  0x0b0bddc1 in ?? ()
#2  0x00dfc09f in ?? ()


### sc...@gmail.com (2011-03-03)

Affects M9; fix in M10.

### sc...@gmail.com (2011-03-03)

[Empty comment from Monorail migration]

### er...@gmail.com (2011-03-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-30)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### sc...@gmail.com (2011-03-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/74662?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088408)*
