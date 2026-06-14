# v8 fuzzing 1122 - stack corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40088411](https://issues.chromium.org/issues/40088411) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-03-02 |
| **Bounty** | $1,000.00 |

## Description

http://code.google.com/p/v8/issues/detail?id=1122

Using a IA32 ret instruction with an immediate that is too big for the encoding. This will corrupt the stack and is *bad*.

This still needs to be confirmed or disproved.

## Timeline

### sk...@chromium.org (2011-03-02)

It looks like this could cause stack corruption because the uint16 used in a "ret XX" wraps, causing the code to not pop enough arguments off the stack. The function returned to will use attacker supplied data as its stack.

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-02)

There's a hard CHECK here for a an over-sized immediate. So, unless I misunderstand the current state, we'll terminate execution before the stack can ever get corrupted. So, this shouldn't be a security issue, but please adjust if I'm wrong.

### js...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-03)

Does not seem to affect M9

### er...@gmail.com (2011-03-03)

[Empty comment from Monorail migration]

### wh...@chromium.org (2011-03-03)

In the versions of assembler-ia32.cc and assembler-x64.cc at the time of the bug report, the CHECK was only an ASSERT, so the release build could proceed past that point and generate a corrupt stack.

### sk...@chromium.org (2011-03-03)

Thanks William!

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

This issue was migrated from crbug.com/chromium/74666?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088411)*
