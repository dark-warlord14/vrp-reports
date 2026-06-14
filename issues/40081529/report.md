# Memory corruption in :first-letter rendering

| Field | Value |
|-------|-------|
| **Issue ID** | [40081529](https://issues.chromium.org/issues/40081529) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-06-11 |
| **Bounty** | $500.00 |

## Description

Another interesting bug from Wushi

affects chrome 5.0.375.70. inside debugger hits         ASSERT(obj->isRenderInline() || obj == this); (d:\chrome\375\src\third_party\WebKit\WebCore\rendering\RenderBlockLineLayout.cpp) which is similar to some other bugs i have seen resulting in memory corruption.

Does not affect chrome 6 trunk. Need to hunt down the recent fixes and then probably merge to branch. the fix happened between safari nightly r59670-
r59189

## Attachments

- [wushi509.xhtml](attachments/wushi509.xhtml) (text/html; charset=utf-8, 1.5 KB)

## Timeline

### in...@chromium.org (2010-06-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-11)

I'm increasingly frustrated that particular ASSERT isn't the condition for the while loop there. Changing the behavior would stop a lot of potentially exploitable conditions, but I expect a lot friction upstream to that change.


### [Deleted User] (2010-06-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-22)

Aha!! I was able to finally locate what it fixed it. http://trac.webkit.org/changeset/59247. I tested it locally and it works :). Moving milestone back to 5 since we can now merge in next v5 patchset with alongwith svg memory corruption stuff.

### in...@chromium.org (2010-06-22)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-28)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-06-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=51014 

------------------------------------------------------------------------
r51014 | inferno@chromium.org | 2010-06-28 12:16:35 -0700 (Mon, 28 Jun 2010) | 24 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/RenderBlock.cpp?r1=51014&r2=51013

Merge 59247 - https://bugs.webkit.org/show_bug.cgi?id=38891

Reviewed by Darin Adler.

First-letter had a number of bugs that were exposed by my attempt to optimize the setting of styles when updating first-letter.
The code that drills down to find the first-letter child stopped if it hit an element that didn't need layout.  This means it could
return random incorrect results (and cause the first-letter object to not be found).

In addition when the first-letter was floated/positioned, the text child was not correctly returned, but the container itself was
returned instead.

Finally, the updating code was leaving the box that wrapped the first letter text with a stale style.  The old code happened to work because
it made new styles for the text elements instead of using the enclosing box style.  The regression was caused by my change to make the
text children simply share style with their parent (thus making the bug that the parent had the wrong style become more prominent).

No new tests, since there's a timing component to reproducing the issue.

* rendering/RenderBlock.cpp:
(WebCore::RenderBlock::updateFirstLetter):


BUG=46360
TBR=hyatt@apple.com
Review URL: http://codereview.chromium.org/2842032
------------------------------------------------------------------------


### sc...@gmail.com (2010-07-01)

Thanks for the info wushi! Although this bug was already fixed on WebKit trunk, we weren't aware of it so this qualifies for another reward!

### sc...@gmail.com (2010-07-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-12)

Payment on its way.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/46360?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/46458]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081529)*
