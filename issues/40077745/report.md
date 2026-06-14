# Security: Origin bypass by writing window.frames[i]

| Field | Value |
|-------|-------|
| **Issue ID** | [40077745](https://issues.chromium.org/issues/40077745) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ka...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2013-07-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The window[0],..,window[n] properties on a web page (more commonly accessed as frames[i]) usually contains the active frames on the page. As such, this pseudo-array contains only Window objects, a frame can be added or deleted from it but overwriting window[i] does not make sense and should normally be disallowed.

On Chrome 27 (and a couple of other versions I tested), window[i] can be overwritten by an arbitrary object.  

Try: window[0] = {a:1} on a page that has any iframe in it.

What turns this into a big security hole is that any value written into window[i] becomes accessible to \*any\* other frame on \*any\* origin. This is a bug. I suspect it is designed this way because the other frame is allowed to read window.frames[i] (=== windows[i]) and Chrome does not check whether window.frames[i] has been modified after the frame was started (specifically, it does not check whether it was changed to a non-Window object.)

As you can imagine, this punches a hole through the Same-Origin Policy: any frame on any origin can read/write variables, call functions, and send/receive objects on any other frame, via window[i].

This has serious security implications: it is a new XSS vector, it enables data exfiltration, it may allow  

authentication bypass on applications that rely on cross-frame communication, and more generally, it enables scripts on different origins to pass objects to each other without any checks in between.

Two concrete exploits:

From the viewpoint of a hosting website, the main risk is XSS and data exfiltration. If an attacker frame can convince the website to set a variable to this[i] (or window[i] or top[i]) then this variable becomes a gateway through which any frame can inject code into the website and steal data.  

(See <http://prosecco.inria.fr/iframes.html> for a demo.)

From the viewpoint of hosted frames, the risk is authentication bypass. The single sign-on solutions of Facebook and Google Plus both rely on cross-frame communication to pass authentication tokens. A typical scenario is to have two frames from Facebook/Google hosted on a (potentially malicious) website. The first frame finds the second frame and calls a function inside it to deliver the token. The assumption is that the browser would forbid the function call if the target frame is on a different origin. In our experience, this sort of cross-frame can-i-access-document check is quite common for security components. The vulnerability shown here can lead to bypassing this check. E.g. suppose the hosting website sets:  

window.frames[i] = {document: document, location: whatever}  

Then any frame looking for another frame from its origin can be fooled into thinking it is calling a function from its own origin but is in fact calling the parent.

A minor mitigation: the bug above only appears to apply to window[i] where i is an integer. If a window is accessed through an id e.g. window['id1'] then modifying this property (still allowed) does not result in other frames being able to read it. This gives some protection to honest frames trying to access other frames from their own origin. If they use string identifiers for frames rather than iterating through the frames pseudo-array, they will not accidentally access a non-Window object or trigger any functions.

**VERSION**  

Chrome Version: 27.0.1453.116  

Operating System: MAC OS, Windows

**REPRODUCTION CASE**  

For a Proof-Of-Concept Demo, see <http://prosecco.inria.fr/iframes.html>

The relevant code (simplified) is:  

[Parent Frame]

<iframe src="child-origin"></iframe>
<script>window[0] = {a:"1", f:function(){alert("Child called parent.f()");}}</script>

[Child Frame]

<script>
alert(parent[0].a);
parent[0].f();
</script>

The POC demo also shows how code can be injected into the parent.  

I have also tested the dual case, and yes, the parent can access the child too, if it writes to its own windows[i].  

More generally, a frame can exploit this bug across any number of honest frames  

E.g. top.frames[i].frames[j].....frames[0].f() would still work.

## Timeline

### lc...@google.com (2013-07-07)

In general, SOP does not guarantee any strong isolation between two cooperating sites, and if I understand your PoC, cooperation is required to access the properties of methods exposed by the parent frame.

Nevertheless, it does seem rather unexpected and may be indicative of another problem.

### ka...@gmail.com (2013-07-07)

I called it an SOP bypass because two scripts on different origins are able to share full objects (and functions), not just serialized JSON values. XSS was the first thing I though of but like you say, it may be indicative of other problems.

> if I understand your PoC, cooperation is required to access the properties of methods exposed by the parent  frame.

Not exactly. The POC only requires one frame to make a mistake by writing accidentally to window.frames[i].
The other is completely innocent. 



---
EXAMPLE SCENARIO:
One frame (say top) writes to window.frames[0], e.g. frames[0] = {document: this.document}
The other accesses it as top.frames[0].document, and instead of getting a cross-origin error, which is what it expects (and catches), it gets a valid document and is XSSed.

So the first frame is at fault, not the second. 
----

More generally, one may think of ways the first frame is fooled into writing an innocuous and untainted (even empty) object into this[i] (where i is an integer). That would enable any other frame to get into the first frame
and start injecting code. 





### ts...@chromium.org (2013-07-08)

[Empty comment from Monorail migration]

### ab...@chromium.org (2013-07-08)

Very cool!

### ke...@chromium.org (2013-07-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-07-08)

Tidying up a little. I'm not sure this is severity high; you'd have to find a victim site that assigns to window.frames[i], and I don't expect that there are many of these because such code leads directly to an error on other browsers (well, at least FF).

Nonetheless, it is cool, as Adam points out.

### ka...@gmail.com (2013-07-08)

Thanks.

The "example scenario" above looks at the dual case. A malicious website
sets its own frames[i] to fool an iframe that is trying to find a sibling
from the same origin.

This pattern seems to be common in cross-domain proxies, like those used
with Facebook and Google plus single sign-on but luckily (?)  both of these
use ids to find their siblings and not integer indexes. Using the latter
would trigger the current issue and result in access token leaks/
authentication bypass.

### ab...@chromium.org (2013-07-08)

Yeah, you can use this technique to "set a trap" by faking out your own properties.  Medium is a reasonable rating because there are some preconditions to the attack rather than being a straight UXSS.

### ts...@chromium.org (2013-07-08)

Assigning to Nate.  I've taken a look at this but am not sure about the best way of fixing this.

### pa...@chromium.org (2013-07-08)

CCing Android browser people who are wondering what our plan is for fixing it.

### ja...@chromium.org (2013-07-08)

This is probably a better fit for abarth.

### ab...@chromium.org (2013-07-09)

It's a V8 bug:

https://codereview.chromium.org/18402007

### ab...@chromium.org (2013-07-09)

[Empty comment from Monorail migration]

### ab...@chromium.org (2013-07-09)

I'm also going to update the Blink code as defense in depth: https://codereview.chromium.org/18558007

### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### ab...@chromium.org (2013-07-10)

The V8 CL has landed:

https://code.google.com/p/v8/source/detail?r=15610

It's going to take a bit to roll into Chromium.

### in...@chromium.org (2013-07-10)

Thanks Adam! v8 is destined to roll :) We can close :)

### bu...@chromium.org (2013-07-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=153929

------------------------------------------------------------------------
r153929 | abarth@chromium.org | 2013-07-10T21:18:52.918129Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/v8/custom/V8WindowCustom.cpp?r1=153929&r2=153928&pathrev=153929

Make indexedSecurityCheckCustom more robust

I don't know any way in which this change is observable, but this CL makes
indexedSecurityCheckCustom match namedSecurityCheckCustom in form.

BUG=257748
R=adamk

Review URL: https://chromiumcodereview.appspot.com/18558007
------------------------------------------------------------------------

### pa...@chromium.org (2013-07-11)

[Empty comment from Monorail migration]

### ab...@chromium.org (2013-07-11)

@inferno: Do you know how to merge this CL to the release branches?  I don't have commit rights to the v8 repo...

### in...@chromium.org (2013-07-11)

We ask someone in the v8 team to handle the merges for us, since we don't have commit rights either. I cced danno@, mstarzinger@ already :)

### in...@chromium.org (2013-07-18)

Danno@, Mstarzinger@, can you please help to merge this to v8 m28 and m29 branches. m28 patch 1 is going out next week, so merge is required :)

### ms...@chromium.org (2013-07-22)

Done. Has been merged back to M28 and M29 branches.

https://code.google.com/p/v8/source/detail?r=15801
https://code.google.com/p/v8/source/detail?r=15799

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-07-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=154714

------------------------------------------------------------------------
r154714 | abarth@chromium.org | 2013-07-23T03:42:12.145621Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-window-index-assign-expected.txt?r1=154714&r2=154713&pathrev=154714
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-window-index-assign.html?r1=154714&r2=154713&pathrev=154714

Test assignment to indexed window properties

The actual bug here was fixed in V8, but we should have a test at the Blink
layer too.

R=adamk
BUG=257748

Review URL: https://chromiumcodereview.appspot.com/19923006
------------------------------------------------------------------------

### sc...@gmail.com (2013-07-23)

@karthik.bhargavan: thanks for the report! It's our pleasure to issue you a $500 reward under the Chromium VRP.

### ka...@gmail.com (2013-07-31)

@scarybeasts and the award panel: Thanks for the gesture.

Shall I assume that the V8 fix applies to all versions of Chrome (iOS, Android,...)?
I separately reported this issue to Android Browser: shall I assume they will inherit the same fix, or do I need to follow it up with them separately?

For posterity, I will note here the most likely immediate exploits for the current issue. 
I wrote these in an email to cevans and abarth, and am pasting them here as documentation:
-----
As others have noted in the discussion, there are preconditions to this issue being exploited, and it is difficult to know how many websites use a programming pattern that exercise this vulnerability.
I don't particularly want to go hunting for exploits, but a cursory search through scripts loaded on mozilla, hulu, and wordpress, yielded several examples of third-party iframes looking through their parents frames using parent.frames[0]... Any such iframe can be entrapped by a malicious website using the current issue, leading to some forms of XSS and/or data exfiltration.

See lines 62-67 of https://github.com/lloyd/winchan/blob/master/winchan.js for the vulnerable use in Mozilla Persona (for the cross-domain messaging of sensitive login credentials).
Similar code exists in the Twitter Follow button (around line 565 in prettified version) and in the WordPress likes plugin.

I could be wrong, but at first glance, it seems that these pieces of code were written specifically with IE in mind (otherwise the child iframe could simply look for its sibling iframe by name or id).
Still, I would hazard that there are enough cases where this code would also be executed in Chrome (say, if a user-agent switcher is being used, or if the browser-detection code is flawed.)
-----

Best,
Karthik

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

This issue was migrated from crbug.com/chromium/257748?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077745)*
