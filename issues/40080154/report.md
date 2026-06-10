# Security: Cross-origin information leak via ECMAScript harmony proxies

| Field | Value |
|-------|-------|
| **Issue ID** | [40080154](https://issues.chromium.org/issues/40080154) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | we...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2014-08-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Harmony proxy can be used for cross-origin info theft in certain situations like the one shown below.  

Currently harmony proxy is disabled by default and can be enabled by chrome://flags/#enable-javascript-harmony.  

It means this is not a risk for now, but I am reporting it to avoid a future risk.

**VERSION**  

Chrome Version: 36.0.1985.125 m (production release)  

Operating System: Windows 7 SP1

**REPRODUCTION CASE**  

Let's suppose victim's web page serves CSV (or some text-like data).

<!-- \\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\* http://victim/test.csv \\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\* -->
<?php
header('Content-Type: text/csv; charset=UTF-8');
header('Content-Disposition: attachment; filename="test.csv"');
?>

foo,bar,123

Attacker's page steals this CSV by utilizing harmony proxy.

<!-- \\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\* http://attacker/ \\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\*\\* -->
<body>
<script>
window.\_\_proto\_\_ = Proxy.create({
get: function(target, name) {console.log("data=" + name)}
});
</script>
<script src="http://victim/test.csv"></script>
</body>

Attacker's page prints "data=foo" and "data=bar" in the console.

Note that we can thwart this type of attack by "X-Content-Type-Options: nosniff" header  

(That is the very reason why the header was introduced).

## Timeline

### me...@chromium.org (2014-08-04)

Thanks for the report. This seems to be a high severity bug since this is a SOP bypass, although it can be mitigated with nosniff.

@danno, could you please take a look or reassign?

### me...@chromium.org (2014-08-04)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-08-05)

(Not sure why I marked it as medium)

### me...@chromium.org (2014-08-07)

CC'ing a few more people. Could you please take a look or reassign?

### ya...@chromium.org (2014-08-07)

[Empty comment from Monorail migration]

### ro...@chromium.org (2014-08-08)

Since V8's branch for M38 has to be stabilised today, and there is no way of addressing this properly in this short amount of time, we decided to partially disable proxy support. That is, for the time being, --harmony no longer implies --harmony-proxies, and neither does the "Experimental JavaScript" flag in Chrome. Proxies are still available by passing --harmony-proxies explicitly.

(See https://codereview.chromium.org/453903002/)

### ya...@chromium.org (2014-08-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### er...@google.com (2014-08-11)

On a related issue elsewhere, Allen Wirfs-Brock comments

"As far as ES6 is concerned, it is the implementation that defines whether the global object is an ordinary object or an exotic (eg, Proxy) object and also the shape and nature of the Global Object's [[Prototype]] chain.

From an ES6 perspective it would be perfectly valid for an implementation (eg, the browser platform) to restrict modification of the Global Object's [[Prototype]] chain or to restrict what sort of objects can be placed upon it."

I agree.

### er...@google.com (2014-08-11)

Since writing that, I no longer agree. On a related issue elsewhere, someone points out that getters/setters produce similar hazards, so Allen's approach does not solve the problem.

This problem is not browser specific. How can we arrange to have one joint conversation about this rather than several disjoint ones?

### ya...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### we...@gmail.com (2014-08-15)

As mentioned in the thread (#2) somewhere, getter attack involves exhaustive search. You can also employ binary search in getter attacks, but it requires many getters set to the global window object at a time, which result in consuming a lot of client's memory. That means getter attack will not be realistic at all when the target value has just several ten bits of entropy.

On the other hand, harmony proxy attack does not have such limitation. So I don't think the difference (in terms of the risk) between the two attack methods is small... or am I misunderstanding something?


### er...@google.com (2014-08-15)

> That means getter attack will not be realistic at all when the target value has just several ten bits of entropy.

That means it will be realistic when the target has less entropy. That means that victims should not assume they are safe from the attack unless they know that their genuine entropy exceeds the attacker's budget. Potential victims are in a poor position to estimate their genuine entropy, because that depends on how much the attacker may already know about them.

Better to just recommend "X-Content-Type-Options: nosniff"[1], rather than encourage a false sense of security by "mitigating" problems we don't solve.

That said, there's nothing in principle wrong with Allen's mitigation, as long as people don't mistake it for having usefully defended anything.

[1] We should also make "X-Content-Type-Options: nosniff" a de jure std and ensure it is adequately implemented across browsers. See https://bugzilla.mozilla.org/show_bug.cgi?id=471020

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-14)

Bulk update: removing view restriction from closed bugs.

### er...@gmail.com (2015-01-22)

https://bugzilla.mozilla.org/show_bug.cgi?id=1048535 is now public as well.

### ti...@google.com (2015-01-22)

Congratulations - $1000 for this report. Notes from the reward panel: "Harmony Proxy is disabled by default, mitigating the impact. $500 for bug + $500 for the proof of concept code".

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### li...@chromium.org (2015-10-13)

Georg Neis is looking at re-enabling proxies, so this is again a concern.

However, Brian Terlson (ECMAScript spec editor--this is an open web spec security issue) pointed out that browsers refuse to run code in script tags as Javascript if the mimetype isn't Javascript. This is indicated in the HTML spec with this language https://html.spec.whatwg.org/#attr-script-src :

 The value of the [src] attribute must be a valid non-empty URL potentially
 surrounded by spaces identifying a script resource of the type given by the
 type attribute, if the attribute is present, or of the type "text/javascript",
 if the attribute is absent.

Here's an example he made demonstrating it not working with the incorrect mimetype: http://codepen.io/anon/pen/BodJQW . This security issue is all about getting things from other origins where the other origin isn't collaborating (otherwise it could just be JSONP, which is a lot more straighforward), so a non-collaborating origin will just use mimetypes appropriately and only mark things as 

Thanks Toon for raising this issue again.

Given the way that mimetypes work with respect to scripts, would we be OK with shipping proxies, or do we still have concerns about cross-origin violations?

### li...@chromium.org (2015-10-13)

Looks like Mozilla's resolution was to lock down the prototype chain of the global object, to prevent inserting a proxy.

Discussion leading to that decision: https://bugzilla.mozilla.org/show_bug.cgi?id=1048535
Patches for locking it down: https://bugzilla.mozilla.org/show_bug.cgi?id=1052139

The patches are just going in over the past few days, so it's not entirely clear whether it's web-compatible. Probably, if this is the approach we want to go with too, we should get a change into HTML to make it standard.

### li...@chromium.org (2015-10-13)

Javascript MIME type is defined here:

https://html.spec.whatwg.org/#javascript-mime-type

Basically, there's an enumerated list of mimetypes which are interpreted as Javascript, and a list of things that are guaranteed to not be a script, and other things may optionally be interpreted as another scripting language.

That leaves the door open to, say, text/csv being interpreted as some other scripting language, which might lead to this path, even if it's not a Javascript MIME type. However, Chrome and Edge don't do that, and probably all other browsers do as well. One possible simple spec fix would be to further lock down what is considered a script MIME type so as to disallow this sort of cross-origin access in all cases that we are concerned about. Or maybe the spec is already restrictive enough. Thoughts?

### li...@chromium.org (2015-10-13)

[Empty comment from Monorail migration]

### mk...@chromium.org (2015-10-14)

I would not be sad if we further locked down the MIME types that we accept as JavaScript. We've had limited success in that regard by blocking `image/*`. Perhaps we could go further and block unknown `text/*`, though we'd need to add some metrics first.

We need to add those metrics though, because "a non-collaborating origin will just use mimetypes appropriately" is simply wrong. The internet is broken in a wide variety of ways, and assuming that servers are Doing The Right thing is almost always incorrect. :P

### li...@chromium.org (2015-10-28)

[Empty comment from Monorail migration]

### li...@chromium.org (2015-10-28)

After talking with Adam Klein, my concern is that people might use text/plain a lot for both JS and CSV. I think adding metrics is a good idea.

### jw...@chromium.org (2015-10-29)

I agree with Mike that the best thing would be to lock down script MIME types even more, but I have a deep fear that the metrics won't bear that out.

Here's a Crazytown idea that littledan@ and I discussed offline: What if we added strict MIME type restrictions for JavaScript *only* in the case that a Proxy exists? So if you're using this cool-awesome-new-feature, you'll essentially be opting into stricter MIME type checking, which is fine, because this would only apply to new code. As littledan@ also pointed out, it would probably be sufficient to have this requirement only if there is a Proxy in the prototype chain of the global object.

adamk@ pointed out that this will be a stronger coupling between V8 and the ScriptLoader than we're used to, so I don't know if this is really a good idea or not.

### ad...@chromium.org (2015-10-29)

The narrow version of #27, where we restrict mime types only if there is a Proxy in the prototype chain of the global object, sounds plausible to me (if rather messy).

I don't think the weaker version ("a Proxy exists") would work, if the metrics are as we suspect and lots of script is loaded with the wrong mime type, since a Proxy somewhere in the object graph isn't necessarily in direct control of the site operator (that Proxy could have been created by some third-party script).

### ha...@google.com (2015-11-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6f9d55e0e902b20bcb8a38be6721f498a2a973ab

commit 6f9d55e0e902b20bcb8a38be6721f498a2a973ab
Author: littledan <littledan@chromium.org>
Date: Wed Dec 09 08:54:57 2015

Add counters for various ways of loading scripts with bad mimetypes

Unchecked use of proxies could enable cross-origin reading of some CSV
files which contain sensitive non-numerical information. Tightening
down mimetype checking could provide a mitigating strategy. This patch
adds UseCounters to see how often scripts are used with different
mimetypes to determine what could be prohibited.

BUG=chromium:399951
R=adamk

Review URL: https://codereview.chromium.org/1413193010

Cr-Commit-Position: refs/heads/master@{#364013}

[add] http://crrev.com/6f9d55e0e902b20bcb8a38be6721f498a2a973ab/third_party/WebKit/LayoutTests/http/tests/mime/javascript-mimetype-usecounters-expected.txt
[add] http://crrev.com/6f9d55e0e902b20bcb8a38be6721f498a2a973ab/third_party/WebKit/LayoutTests/http/tests/mime/javascript-mimetype-usecounters.html
[add] http://crrev.com/6f9d55e0e902b20bcb8a38be6721f498a2a973ab/third_party/WebKit/LayoutTests/http/tests/mime/resources/javascript-mimetype.php
[modify] http://crrev.com/6f9d55e0e902b20bcb8a38be6721f498a2a973ab/third_party/WebKit/Source/core/dom/ScriptLoader.cpp
[modify] http://crrev.com/6f9d55e0e902b20bcb8a38be6721f498a2a973ab/third_party/WebKit/Source/core/dom/ScriptLoader.h
[modify] http://crrev.com/6f9d55e0e902b20bcb8a38be6721f498a2a973ab/third_party/WebKit/Source/core/frame/UseCounter.h


### li...@chromium.org (2015-12-16)

It could take a month or two until we have reliable data from those UMA counters in order to decide what we should do about these cross-origin subresource loads. Let's wait to stage Proxies until we have the policy in place, so we don't put experimental JS features users at risk of this security issue.

### ha...@chromium.org (2015-12-16)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-12-16)

Adding blocked on relationship because we cannot define the reverse.

### bu...@chromium.org (2015-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/01b8e7c7f62fe0fc74552c7d3909777fa50b3447

commit 01b8e7c7f62fe0fc74552c7d3909777fa50b3447
Author: verwaest <verwaest@chromium.org>
Date: Thu Dec 17 14:37:16 2015

Throw TypeError when reading global references through a JSProxy

Allowing global references to be read through a proxy results in cross-origin information leaks. The ES6 spec currently does not mitigate this in any way. This CL adds a workaround that's easy for V8: throw whenever an unresolved reference would result in a proxy trap to be fired. I'm landing this so we can move forwards with staging proxies without putting users of --harmony at risk.

BUG=chromium:399951
LOG=n

Review URL: https://codereview.chromium.org/1529303003

Cr-Commit-Position: refs/heads/master@{#32949}

[modify] http://crrev.com/01b8e7c7f62fe0fc74552c7d3909777fa50b3447/src/messages.h
[modify] http://crrev.com/01b8e7c7f62fe0fc74552c7d3909777fa50b3447/src/objects.cc
[add] http://crrev.com/01b8e7c7f62fe0fc74552c7d3909777fa50b3447/test/mjsunit/harmony/proxies-global-reference.js


### li...@chromium.org (2015-12-19)

Unfortunately, early data seems to already show that the mimetype lockdown I was hoping for won't be possible. In Chromestatus, you can see

https://www.chromestatus.com/metrics/feature/popularity#CrossOriginTextScript

the counter for cross-origin subresource loads of scripts with a mimetype starting with 'text', without the rest of the mimetype being a proper JavaScript mimetype, is already above 0.03% even though these counters have only rolled out to a small percentage of users (by comparison, sloppy mode, whose counter I put in at the same time, is at 0.46%, so you might scale this up to be around 7% of web pages making such a bad request).

We'll probably need to go with a more exotic approach. Quick summary of ideas:
- Toon's idea: No global reference through JSProxy
- Firefox's idea: Lock down the window's prototype chain
- JWW's idea: Add mimetype restrictions just when there's a Proxy, or just when there's a proxy in the prototype chain of the global object (either test would have to be done at the beginning of script execution, to account for async script loads/compilation).

All of these would require significant hooks with the way JavaScript is executed.

### er...@google.com (2015-12-19)

I like 

> - Firefox's idea: Lock down the window's prototype chain

best. There's no good reason to make window inherit from a proxy, and this would be the most local of these workarounds.

### ve...@chromium.org (2015-12-19)

The only issue I see with FF's approach is that it will lock down Object.prototype, possibly breaking existing code. Either that, or you make window use a copy of Object.prototype in its chain. That might again break existing code (e.g. due to "instanceof Object").

"My approach" is mostly the most careful one wrt not breaking existing code. It doesn't nicely fit into the current spec though.

If FF approach works without breaking the web, I have no issue with switching to it.

### bu...@chromium.org (2015-12-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/28523e2cf18ee02f503e1792788b88d828968055

commit 28523e2cf18ee02f503e1792788b88d828968055
Author: noel <noel@chromium.org>
Date: Sat Dec 26 21:56:26 2015

http/tests/mime/javascript-mimetype-usecounters.html is flaky

TBR=jochen@chromium.org,littledan@chromium.org
NOTRY=true
BUG=399951

Review URL: https://codereview.chromium.org/1544303002

Cr-Commit-Position: refs/heads/master@{#366909}

[modify] http://crrev.com/28523e2cf18ee02f503e1792788b88d828968055/third_party/WebKit/LayoutTests/OilpanExpectations
[modify] http://crrev.com/28523e2cf18ee02f503e1792788b88d828968055/third_party/WebKit/LayoutTests/TestExpectations


### li...@chromium.org (2015-12-30)

The discussion at https://github.com/tc39/ecma262/issues/272 seems to be strongly in the direction of Firefox's approach of freezing the prototype chain of the global object so a Proxy can't be inserted. It's unclear whether we'll be adding a general MOP operation or just doing a one-off change for the things in the prototype chain of the global object, though.

For now, I think it'd be fine to ship Proxies with Toon's current security policy. The new proposed policy adds strictness only in other areas of the language (mutating the prototype chain) and doesn't add strictness with respect to when Proxies are used. Since we won't be taking away anyone's capabilities to use Proxies, it seems fine to me to have this intermediate policy at first.

If anyone wants to get started on shipping the eventual policy, I'd start by implementing a way to have immutable prototypes, calling it on Object.prototype and exposing it to Blink to call on other things in the global proto chain. Just the builtin stuff. It's unclear whether this will be something that's added to the metaobject protocol (with Reflect and maybe Proxy support), but we seem to have consensus for this being the basic part.

That is, as long as this new policy turns out to be web-compatible!

### li...@chromium.org (2016-01-29)

At TC39 this week, we reached consensus on Mozilla's global object proto chain freezing proposal. I have a pull request out against the ECMAScript spec which I expect to be merged in some form soon at https://github.com/tc39/ecma262/pull/308#discussion_r50484415 . Mozilla has already shipped this in Stable with no web compatibility issues. I think we should try to implement this in Chrome soon.

### li...@chromium.org (2016-03-25)

The change to the ES spec was made, and it is part of ES2016. Now this needs to be implemented--both freezing Object.prototype.__proto__ and the equivalent for window and location. Once that is done, we can remove the temporary approach which currently blocks individual global object reads through Proxy.

### li...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### br...@gmail.com (2017-02-03)

littledan@chromium.org did this reach a point where the temporary approach could be removed?

### li...@chromium.org (2017-02-05)

bradley.meck, thanks for the ping here--yes, that would be appropriate at this point. Added it to my todo list.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/399951?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/1543, crbug.com/v8/5149]
[Monorail components added to Component Tags custom field.]

### ch...@chops-service-accounts.iam.gserviceaccount.com (2025-06-03)

The unexpected pass finder removed the last expectation associated with this bug. An associated CL should be landing shortly, after which this bug can be closed once a human confirms there is no more work to be done.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080154)*
