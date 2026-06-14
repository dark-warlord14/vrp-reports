# Javascript execution bug introduced with Chrome 29.0.1547.57

| Field | Value |
|-------|-------|
| **Issue ID** | [40078019](https://issues.chromium.org/issues/40078019) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | ad...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2013-08-31 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : 29.0.1547.57  

URLs (if applicable) : none  

**Other browsers tested:**  

Safari 6: OK  

Firefox 20: OK  

IE 8/9/10: OK  

Chrome 29.0.1547.62: FAIL  

Chrome 29.0.1547.57 and .62 if code is stepped through in debugger: OK

**What steps will reproduce the problem?**

1. Open the attached file ChromeTest.html in Chrome 29. This file contains a javascript function that recursively wraps any non-function properties of an object with a function expression (function () { return value; }). It then tests the returned object with some assertions to see if the mapped object contains the expected values.

**What is the expected result?**  

All assertions should pass. They do on FF, IE and Safari. They also do in Chrome 29 if you step through the code in the debugger. Only if you let it run does it display the issue. Optimization and/or JIT bug?

**What happens instead?**  

Two of the assertions fail, regarding a property (B) that was a function to start with but which is now mysteriously set to the value of the next property processed, and that next property (C), which becomes undefined.

Discussion/Discovery  

We were contacted by our users saying several applications we wrote using knockout.js had started failing after Chrome autoupdated to version 29.0.1547.57. After some probing, we found that the specific problem was with knockout's mapping plugin. If you're not familiar with that plugin, it recursively converts the properties of an object to knockout's ko.observable type, so that they may be bound to the DOM. With Chrome 29, some of the properties were being scrambled (coming back with values from different properties), and some were coming back undefined. The plugin works correctly in all other browsers which we have tested.

We started paring down the plugin until we could find the smallest case that would repro the issue, which is the attached file.

Also attached is a screenshot of a Chrome Dev tools session showing where the assertions fail.

## Attachments

- [ChromeTest.html](attachments/ChromeTest.html) (text/html; charset=utf-8, 1.8 KB)
- [Chrome29Test.png](attachments/Chrome29Test.png) (image/png; charset=binary, 172.2 KB)

## Timeline

### pd...@gmail.com (2013-09-01)

When you run the function in try/catch (to disable optimisation), it passes also.

### tk...@chromium.org (2013-09-02)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-09-02)

Able to reproduce the issue on win7 chrome version 29.0.1547.57 and beta version 30.0.1599.22

Working fine in chrome version 31.0.1618.0 and latest 31.0.1619.1 canary Aura

@kbr, Can you please let us know if further bisect is needed for this issue.

### kb...@chromium.org (2013-09-03)

+a couple of V8 team members


### jk...@chromium.org (2013-09-03)

Thanks for providing such an excellent test case!

The issue (or at least the test case) was fixed by https://chromiumcodereview.appspot.com/22911018. Assigning to verwaest@ to decide if that's safe enough to backmerge, or if we can develop a simpler version of that fix, or if the bug is actually elsewhere and was just hidden by this refactoring.

### ve...@chromium.org (2013-09-06)

This is definitely a quite severe security bug. It allows javascript code to (at least) mutate whatever object pointer is the first two words after the header of an object by writing a constructed double into it (can be easily be constructed to be anything since those doubles can be loaded from typed arrays).

I have a reduced bugfix, but it doesn't have any canary coverage yet though. Either way is fine for me: Merge the entire patch back, including the bugfix, which has canary coverage; or merge the following fix back (without coverage?): https://chromiumcodereview.appspot.com/23897004

### ve...@chromium.org (2013-09-06)

[Empty comment from Monorail migration]

### ve...@chromium.org (2013-09-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-18)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### ve...@chromium.org (2013-09-18)

Marking as fixed since the reduced bugfixes were merged back to both M29 and M30.

### in...@chromium.org (2013-09-18)

[Empty comment from Monorail migration]

### ve...@chromium.org (2013-09-18)

Apparently, unfortunately, the fix wasn't picked up by the latest M29. It's using V8 3.19.18.23, while the patch was merged as V8 3.19.18.24.

### in...@chromium.org (2013-09-18)

That is ok, we don't have any more m29 patches, so this will go straight to m30.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

Removing incorrect Release-0 which is reserved for bugs impacting stable.

### in...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-26)

Adam.haile, what name would you like us to use when we give you credit for this bug in the release notes on the Chrome blog?

### ad...@gmail.com (2013-09-26)

Thanks!  Adam Haile is fine, and my company is Concrete Data (concretedata.com), if you list that as well.

### mb...@chromium.org (2013-09-26)

Thanks! We will credit you as Adam Haile of Concrete Data.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

Not filed as a security issue, but we still reward for the first time this happens, as it's not always clear.
So, delighted to tag this report with a $1000 Chromium Security Reward.

### ad...@gmail.com (2013-10-01)

That's awesome!  Thanks so much!  Is there anything I need to do to provide payment information?

### pa...@chromium.org (2013-10-18)

Hey Adam, processing via our e-payment system can take a few weeks, but reward should be on its way to you now. Thanks again for your help!

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/282736?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078019)*
