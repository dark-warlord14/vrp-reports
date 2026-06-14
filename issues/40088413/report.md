# v8 fuzzing 1128 - out of bounds write

| Field | Value |
|-------|-------|
| **Issue ID** | [40088413](https://issues.chromium.org/issues/40088413) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-03-02 |
| **Bounty** | $500.00 |

## Description

Upstream http://code.google.com/p/v8/issues/detail?id=1128

Mads: receiver of JS function call not properly converted to Javascript Object, could cause a crash (or otherwise) in generated code by causing it to read from an arbitrary pointer.

JSchuh: exploitable write

## Timeline

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-03-02)

There is no (direct) write here, but an out of bounds read.

V8's values are either a 4-byte aligned pointer into V8's heap, tagged by adding 1; or else a 31-bit integer tagged by shifting left by one so it has a zero in the low-order bit.

The first word of a V8 heap-allocated object gives metadata about the object.  Normally, before reading this word from a V8 value, we will check that it is actually a heap object and not tagged integer.  In a few places we specialize code to skip the integer check (because we know it's always been already performed).

This bug bypassed one of those integer checks.  We would take an arbitrary V8 value, subtract one (to remove the heap object tag) and read the word at that location.

One could supply *any* 31-bit number and have it treated as a 32-bit address by shifting left and subtracting one, that we would then read from.

The read value is compared to an expected constant, which is unpredictable.  If the value doesn't match, we would go into V8's runtime which should fail more gracefully than the seg fault (I can dig up what it would do if you need).

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-02)

Yeah, my original estimation was "looks like but didn't know." Bumping severity as appropriate. Given the restrictions on the read we me decided to bump it down lower.

### js...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-03-02)

So, after a discussion with Kevin, it seems that if an attacker would very carefully create a structure in memory that looks sufficiently like an object, and passed an integer that pointer to the right location in the structure, v8 would assume that everything is ok.
So, when the function is called, it has an invalid "this" that the attacker controls and which passes v8's checks to see if it is a valid object. This could allow an attacker to read/write to arbitrary memory. Probably very hard to exploit, but not impossible.

### sc...@gmail.com (2011-03-03)

Does not seem to affect M9

### sc...@gmail.com (2011-03-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-30)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

This issue was migrated from crbug.com/chromium/74670?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088413)*
