# UXSS with window.execScript

| Field | Value |
|-------|-------|
| **Issue ID** | [40091101](https://issues.chromium.org/issues/40091101) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | [Deleted User] |
| **Assignee** | ag...@chromium.org |
| **Created** | 2011-05-19 |
| **Bounty** | $3,133.00 |

## Description

This is a breakout of the execScript bug from http://crbug.com/83096

This is already fixed on trunk but will need a merge for m12

## Timeline

### [Deleted User] (2011-05-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-20)

Jason, this is fixed on v8 bleeding_edge. Can you press the magic button to pick it on 742 branch.

### ke...@google.com (2011-05-20)

We don't handle V8 merges, they will need to merge it over.

### ag...@chromium.org (2011-05-23)

I have merge the removal of execScript to Chrome 12 branch (V8 3.2 branch). Be aware that this makes the fast/dom/prototype-inheritance.html layout test fail (because our custom expectations expect execScript).

### js...@chromium.org (2011-05-23)

Thanks Mads.

### sc...@gmail.com (2011-05-23)

[+kareng]
@kareng @mads @inferno @cdn @jshsuh @all :) -- will this make the cut for the (presumably) final M11 patch?

### ag...@chromium.org (2011-05-23)

It is in the M11 V8 branch as of a couple of hours ago so it should be picked up if there is another M11 build.

### js...@chromium.org (2011-05-23)

@scarybeasts - I didn't want to disable the API entirely in a minor release. I figure it's best to pick it up in in m12.

### sc...@gmail.com (2011-05-23)

@jschuh -- that does sound reasonable. However, my question was more from the angle of Mads' comment in https://crbug.com/chromium/83096 (and now https://crbug.com/chromium/83275#c7 above), which states that the change was merged to M11.
Therefore, one critical question is when did Karen kick off the stable build that is planned to be the final M11 patch?

### ka...@google.com (2011-05-23)

i kicked it last thursday so, no, this didn't make it :)

### sc...@gmail.com (2011-05-23)

@mads: thanks for the M11 merge. Looks like it won't see light of day in an M11 release due to no plans to kick off further M11 builds. Not to worry, M12 is getting close :)

### sc...@gmail.com (2011-06-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-03)

@serg.glazunov: congrats! We're rewarding this bug at the top $3133.7 level because you demonstrated critical impact by chaining it together with a bunch of other bugs.

We remain extremely impressed by this achievement.

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

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

Pleasure to pay this one, Serg :)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-11-03)

This issue was migrated from crbug.com/chromium/83275?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/83096]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091101)*
