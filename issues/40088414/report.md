# v8 fuzzing - 1136 - corrupt JIT code

| Field | Value |
|-------|-------|
| **Issue ID** | [40088414](https://issues.chromium.org/issues/40088414) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-03-02 |
| **Bounty** | $1,000.00 |

## Description

http://code.google.com/p/v8/issues/detail?id=1136

incorrect state and address for deoptimization, we can jump into unoptimized code with a stack one word too short.  We can also jump to an incorrect address (still in the unoptimized code, at an ia32 instruction boundary).

## Timeline

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-03-02)

This is actually different from https://crbug.com/chromium/74669 (shortening the stack frame of a javascript function by one).

In this case, we can jump to the wrong instruction in unoptimized code, that does not correspond to where we have deoptimized from.  The instruction will still be one of our deoptimization points (specifically an IA32 instruction boundary).  The state including stack height will be constructed according to the expectation at the place we actually jump to, so there is no stack height problem once we're running in the unoptimized code.

However, the construction of this unoptimized frame state will be based the wrong description of the optimized frame, so the values of the locals, compiler-generated temporary values, and parameters will be corrupted.

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-03)

Does not seem to affect M9

### sc...@gmail.com (2011-03-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-30)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### sc...@gmail.com (2011-03-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-10-03)

This issue was migrated from crbug.com/chromium/74671?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088414)*
