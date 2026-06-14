# Pwnium bug: Prerendering issues with NACL

| Field | Value |
|-------|-------|
| **Issue ID** | [40054746](https://issues.chromium.org/issues/40054746) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | mm...@chromium.org |
| **Created** | 2012-03-10 |
| **Bounty** | $60,000.00 |

## Description

https://chromiumcodereview.appspot.com/9664025/

Need to commit to trunk and m18.

## Timeline

### in...@chromium.org (2012-03-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2012-03-10)

The plugin blocking logic wasn't being run for NaCl in prerendering. Fixed by moving plugin loading in prerendering after the NaCl checks.

### cb...@chromium.org (2012-03-10)

We will also want fixes on trunk and the 18 branch. Code is slightly different on trunk from M17 branch, haven't looked at 18.

### sc...@gmail.com (2012-03-10)

Setting Merge-Approved to indicate that we need to make sure to commit to additional places (trunk, M18).

Actual severity is probably medium, but it chains together with other higher severity issues nicely.

### in...@chromium.org (2012-03-10)

Chris (cbentzel@), please commit the trunk patch next week.

### in...@chromium.org (2012-03-10)

By next week, i meant this coming week. sorry!

### cb...@chromium.org (2012-03-10)

I'm going to assign some other folks to potentially do the trunk and 18 merge. I'm going to be in transit to, and Dominic may need to drop everything work related this coming week, so Matt should be able to do it. 

### sc...@gmail.com (2012-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-12)

I have a patch ready for trunk but want to confirm that it's ok to upload and set to private (restricted to @chromium.org and @google.com).

### mm...@chromium.org (2012-03-12)

I'm working on some regression tests which I thought, out of general paranoia, may be worth merging along with the fix.

### sc...@gmail.com (2012-03-12)

Yes, please land the fix to trunk. Did you want to handle the M18 merge or should we?

### sc...@gmail.com (2012-03-12)

Can you update the bug with status for both trunk fix and M18 merge?


### mm...@chromium.org (2012-03-12)

I have a fix and browser tests for NaCl enabled/disabled.  I just want to make sure the enabled browser tests are non-flaky (The disabled ones I'm sure are).  The the disabled test is flaky, I'll just remove it from the CL.  Either way, I'll submit for review tonight or tomorrow am.

### sc...@gmail.com (2012-03-12)

We need this merged to M18 immediately, otherwise the fix may miss M18 stable.

### sc...@gmail.com (2012-03-12)

Looks like we have a timezone issue :(

I will attempt the M18 merge myself.

### sc...@gmail.com (2012-03-12)

Ok, M18 is http://src.chromium.org/viewvc/chrome?view=rev&revision=126245

Still needs landing on trunk. Hard to know what status to use for the bug.

### sc...@gmail.com (2012-03-12)

Assuming trunk gets taken care of over the next day, I think it's ok to leave the bug in a "nothing needs doing" status for now.

### sc...@gmail.com (2012-03-12)

Better status: mstone=19, merge=approved

### mm...@chromium.org (2012-03-12)

Sorry, I had thought the M18 branch point would be later this week or early next, or I would have let dominich go ahead and land his CL without the tests.

### bu...@chromium.org (2012-03-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=126245

------------------------------------------------------------------------
r126245 | cevans@chromium.org | Mon Mar 12 15:00:42 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/chrome/renderer/chrome_content_renderer_client.cc?r1=126245&r2=126244&pathrev=126245

Merge http://src.chromium.org/viewvc/chrome?view=rev&revision=125947 to M18.

TBR=mmenke
BUG=117620
Review URL: https://chromiumcodereview.appspot.com/9696012
------------------------------------------------------------------------

### [Deleted User] (2012-03-12)

[Comment Deleted]

### sc...@gmail.com (2012-03-13)

I think we have time to wait for tests :)

### bu...@chromium.org (2012-03-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=126718

------------------------------------------------------------------------
r126718 | mmenke@chromium.org | Wed Mar 14 13:25:00 PDT 2012

Changed paths:
 A http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/prerender/prerender_plugin_nacl_disabled.html?r1=126718&r2=126717&pathrev=126718
 A http://src.chromium.org/viewvc/chrome/trunk/src/chrome/test/data/prerender/prerender_plugin_nacl_enabled.html?r1=126718&r2=126717&pathrev=126718
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/chrome_content_renderer_client.cc?r1=126718&r2=126717&pathrev=126718
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/prerender/prerender_browsertest.cc?r1=126718&r2=126717&pathrev=126718
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/plugins/plugin_placeholder.cc?r1=126718&r2=126717&pathrev=126718

Switch ordering of prerender and NaCl allowed checks when creating a plugin.

R=dominich@chromium.org
BUG=117620
TEST=PrerenderBrowserTest.PrerenderNaClPluginDisabled, PrerenderBrowserTestWithNaCl.PrerenderNaClPluginEnabled

Review URL: http://codereview.chromium.org/9677033
------------------------------------------------------------------------

### sc...@gmail.com (2012-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-10)

Pwnium reward paid out!

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### js...@chromium.org (2012-05-21)

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/117620?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054746)*
