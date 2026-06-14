# v8 fuzzing - 1113 - stack corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40088412](https://issues.chromium.org/issues/40088412) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-03-02 |
| **Bounty** | $1,000.00 |

## Description

Upstream http://code.google.com/p/v8/issues/detail?id=1113

Mads:
incorrect state at deoptimization, we can jump into unoptimized code with a stack one word too short.  This invalidates esp-relative addressing (ebp value is unchanged).  It can allow changing the JS function in the frame to an arbitrary value.  If this could be iterated (optimize/deoptimize/optimize/deoptimize/...., but that might not be possible because the next optimization would crash) an attacker could read or write the return address and the caller's frame pointer.
---

BJ:
Being able to read pointers sounds like an ASLR bypass. However, the "crash" mentioned may be more interested - I'll ask Mads. 

## Timeline

### sk...@chromium.org (2011-03-02)

Setting at medium for ASLR bypass for now.

### sk...@chromium.org (2011-03-02)

I overlooked the "write the return address" part :D

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-03-02)

The ia32 stack layout of an unoptimized JS function, at the time in question, should look like (stack grows up):

esp --> local i
        local i-1
          :
        local 0
        context
        function
ebp --> caller's ebp
        caller's eip
        arg j
         :
        arg 0

The locals, context, function, and arguments are all V8 values.  They are 4-byte aligned pointers into V8's heap, tagged by adding 1; or else 31-bit small integers tagged by shifting left by one.

This bug causes us to jump into the unoptimized code with a stack that is too small by one, with esp pointing to "local i-1".  ebp is not affected.

The locals, context, function, and arguments are all accessed based on ebp, so they cannot be used to read values like the caller's ebp (frame pointer) or eip (program counter).

The last local variable, local i is now floating above esp and can be used to give (ebp-relative) access to whatever value happens to be there.  This could be used to read an address in the code object in V8's heap if we call something that doesn't take any arguments.

### km...@chromium.org (2011-03-02)

The crash Mads mentioned is that if we later try to optimize the too-short unoptimized frame, we will not properly set up the last local, "local i" in the optimized stack frame we build.

The optimized code will see the value 0xbeeddead which it will interpret as a valid V8 object.

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

This issue was migrated from crbug.com/chromium/74669?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088412)*
