# OOM handler not always properly terminating process

| Field | Value |
|-------|-------|
| **Issue ID** | [40087136](https://issues.chromium.org/issues/40087136) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-01-21 |
| **Bounty** | $1,000.00 |

## Description

Credit: David Warren of CERT/CC

Thanks to David for his persistence, we appear to have confirmed that OOM (on Windows at least) can continue execution with a "NULL" return value instead of just exiting the process.

I've already fixed the bug: http://src.chromium.org/viewvc/chrome?view=rev&revision=72107

I'm filing this so we can track the announce, credit and need to merge to M9.

## Timeline

### sc...@gmail.com (2011-01-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-23)

Working theory:
- Our exception handler for __debugbreak actually returns instead of exiting the process.
- Cris and I tested this without a debugger attached by adding "while (1);" right after the __debugbreak. We then triggered an OOM, and observed a process spinning on Cris's machine at 100% CPU.

### js...@chromium.org (2011-01-23)

That's very weird. Was this tested against a release or debug build?

### js...@chromium.org (2011-02-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-02-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-02)

Merged to m9 @73390

### sc...@gmail.com (2011-02-02)

This was a very interesting bug; hence it is being rewarded at the $1000 level.

In instances where an individual is unable to accept the reward or nominate a charity, the reward money will go to our default charity of Red Cross.

### sc...@gmail.com (2011-02-03)

Money on way to charity.

### in...@chromium.org (2011-02-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/70456?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087136)*
