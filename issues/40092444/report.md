# The beforeload event allows tracking URI changes in a frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40092444](https://issues.chromium.org/issues/40092444) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ju...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-07-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The beforeload event allows a website to track URI changes that happen inside a frame. By abusing this property, an attacker could gain access to sensitive information and security tokens, enabling further CSRF-style attacks.

**VERSION**  

Chrome Version: 14.0.803.0 dev  

Operating System: Ubuntu 10.04 LTS

**REPRODUCTION CASE**  

The code below opens a Google redirection page in an iframe. The onbeforeload event attribute is used to detect the URL changes.

<iframe
src="http://ssl.gstatic.com/chrome/webstore/html/bounce.html#continue=https%3A%2F%2Fchrome.google.com%2Fwebstore%2F"
onbeforeload="alert('Now opening ' + event.url)">
</iframe>

## Timeline

### in...@chromium.org (2011-07-07)

Looks like this webkit specific feature - http://developer.apple.com/library/safari/#documentation/Tools/Conceptual/SafariExtensionGuide/MessagesandProxies/MessagesandProxies.html#//apple_ref/doc/uid/TP40009977-CH14-SW9 does not handle 302 redirects and keeps updating event.url when it shouldn't ? Perhaps we should freeze event.url ?

Adam, what do you think is the right approach ?

### ab...@chromium.org (2011-07-07)

Ouch.  Yeah, we should only trigger the beforeload event on the original frame load (the one that the attacker knows the URL of).

### ju...@gmail.com (2011-07-10)

Low? Shouldn't this be tagged AT LEAST medium severity? A huge number of unsuspecting websites - including my bank - being exposed to CSRF seems pretty serious to me...

### in...@chromium.org (2011-07-10)

Putting CSRF token in the URL is a bad practice in itself. It can get logged at multiple places like your ISP, etc. Anyway, this is low severity as per the chromium severity ratings.

### ju...@gmail.com (2011-07-10)

According to the severity guidelines, a security issue is of medium severity if it "can be combined with other vulnerabilities to cause harm" and of high severity if it "lets an attacker read or modify confidential data belonging to other web sites". Both are true for this one.

### sc...@gmail.com (2011-07-10)

Yes, this is a Medium.
It's also very similar to much older bug https://code.google.com/p/chromium/issues/detail?id=32309, which we rated as a Medium.

### sc...@gmail.com (2011-07-10)

This may also affect a small number of Google websites.

### ju...@gmail.com (2011-07-10)

scarybeasts: it does, I've already found one instance.

### sc...@gmail.com (2011-07-10)

Out of interest, can you document that instance here?

### ju...@gmail.com (2011-07-10)

<iframe
	src="https://www.google.com/accounts/ServiceLogin?service=writely&passive=1209600&continue=http://docs.google.com/settings"
	onbeforeload="alert(event.url)">
</iframe>

The second alerted URL contains the email address of the currently logged in user, and an 'auth' key, of which I'm not sure what it can be used for.

### ab...@chromium.org (2011-07-10)

Am I fixing this bug, or is someone else?

### in...@chromium.org (2011-07-10)

Adam, it will be awesome if you can please help to fix this.

### sc...@gmail.com (2011-07-10)

I know you're busy Adam, but if you could knock this one down, it would be much appreciated. I was going to look at it, but a few video bugs just came in :-/

### ab...@chromium.org (2011-07-10)

Technically I should be working on gardening tools, but I'm happy to look at this bug.

### sc...@gmail.com (2011-07-10)

What a gentleman :) (There's also evidence of scholarly activity too)

### ab...@chromium.org (2011-07-13)

[Empty comment from Monorail migration]

### ab...@chromium.org (2011-07-13)

The trick is that it needs to be a client redirect.  Server redirects aren't leaked.

### ab...@chromium.org (2011-07-13)

Patch in hand.  Is there no WebKit bug already?  I thought we were supposed to open WebKit bugs as soon as practical.

### sc...@gmail.com (2011-07-13)

Looks like filing of the bug fell between the cracks. Oops.
Since we're turning up with a patch, I'm sure there will be no ill will.

### ab...@chromium.org (2011-07-13)

https://bugs.webkit.org/show_bug.cgi?id=64482

### ab...@chromium.org (2011-07-13)

Oh wait, we're not supposed to use ExternalDependency any more.  Is there a status for "go look in the WebKit bug for the current status" ?

### sc...@gmail.com (2011-07-13)

Not that I know of. "Started" seems good enough; we take it to mean the assignee is all over it :)

I think Abhishek was using "ExternalDependency" for cases where an Apple engineer took a security bug. Seems reasonable because the timescale there is less under our control.

### in...@chromium.org (2011-07-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-15)

r+ achieved upstream :D

Adam, any thoughts on how risky this one is in terms of a merge? (I will take care of the merge if necessary)

### ab...@chromium.org (2011-07-15)

Very safe.  I need to tweak the patch before landing, which I should be able to do tonight.

### in...@chromium.org (2011-07-15)

http://trac.webkit.org/changeset/91044

### sc...@gmail.com (2011-07-16)

Merged to M13: http://trac.webkit.org/changeset/91141

### sc...@gmail.com (2011-07-16)

@juhonurm: how would you like to be credited in our release notes?

### ju...@gmail.com (2011-07-16)

My real name is Juho Nurminen. Use that, please.

### sc...@gmail.com (2011-07-20)

@juhonurm: very interesting bug! Thanks for reporting it. We're happy to offer a provisional $500 Chromium Security Reward for your help.

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

### ju...@gmail.com (2011-07-20)

Cool. Thanks :)

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-28)

@juhonurm: please e-mail cevans@chromium.org for steps to collect your reward

### sc...@gmail.com (2011-11-23)

Payment in system.

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

This issue was migrated from crbug.com/chromium/88337?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092444)*
